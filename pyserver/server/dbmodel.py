from __future__ import print_function
from __future__ import unicode_literals
from builtins import str

import copy
import os
import arrow
import uuid
import json
import pprint

from flask import current_app
from flask_login import current_user

from sqlalchemy.types import TypeDecorator, CHAR, VARCHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import deferred

from validate_email import validate_email

from werkzeug.security import generate_password_hash, check_password_hash

from . import conn

db = conn.db


class GUID(TypeDecorator):
    """
    Platform-independent GUID type. Uses PostgreSQL's UUID type,
    otherwise uses CHAR(32), storing as stringified hex values.
    http://docs.sqlalchemy.org/en/latest/core/custom_types.html
    """

    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class JSONEncodedDict(TypeDecorator):
    """
    Represents an immutable structure as a json-encoded string.
    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class UserDb(db.Model):

    __tablename__ = "users"

    id = db.Column(GUID(), default=uuid.uuid4, primary_key=True)
    username = db.Column(db.String(255))
    name = db.Column(db.String(60))
    email = db.Column(db.String(200))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)
    reset_password_token = db.Column(db.String(255))
    reset_password_expires_on = db.Column(db.DateTime)
    customs = db.relationship("CustomDb", backref="user", lazy="dynamic")

    def __init__(self, **kwargs):
        db.Model.__init__(self, **kwargs)
        self.set_password(kwargs["password"])

    # passwords are salted using werkzeug.security
    def set_password(self, password):
        password = str(password)
        hash = generate_password_hash(password)
        self.password = hash
        print("> UserDb.set_password")
        print("  password: %s (%s)" % (password, type(password)))
        print("  hash: %s (%s)" % (hash, type(hash)))
        print("  self.password: %s (%s)" % (self.password, type(self.password)))

    def check_password(self, password):
        password = str(password)
        print("> UserDb.check_password")
        print("  password: %s (%s)" % (password, type(password)))
        print("  self.password: %s (%s)" % (self.password, type(self.password)))
        new_hash = generate_password_hash(password)
        print("  generate_password_hash: %s (%s)" % (new_hash, type(new_hash)))
        return check_password_hash(self.password, password)

    # following methods are required by flask-login
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class CustomDb(db.Model):

    __tablename__ = "custom"

    id = db.Column(
        GUID(), default=uuid.uuid4, nullable=False, unique=True, primary_key=True
    )
    user_id = db.Column(GUID(True), db.ForeignKey("users.id"))
    custom_type = db.Column(db.Text, default=None)
    attr = db.Column(JSONEncodedDict)
    blob = deferred(db.Column(db.LargeBinary))


# only needs to be done once but here just in case
db.create_all()


def filter_dict_for_none(d):
    new_d = {}
    for key, value in d.items():
        if value is not None:
            new_d[key] = value
    return new_d


def verify_db_session(db_session=None):
    if db_session is None:
        return db.session
    return db_session


def get_server_filename(filename):
    """
    Returns the path to save a file on the server
    """
    dirname = get_user_server_dir(current_app.config["SAVE_FOLDER"])
    if not (os.path.exists(dirname)):
        os.makedirs(dirname)
    if os.path.dirname(filename) == "" and not os.path.exists(filename):
        filename = os.path.join(dirname, filename)
    return filename


# USER functions


def is_current_user_anonymous():
    try:
        result = current_user.is_anonymous()
    except:
        result = current_user.is_anonymous
    return result


def parse_user(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "isAdmin": user.is_admin,
    }


def check_valid_email(email):
    if not email:
        return email
    if validate_email(email):
        return email
    raise ValueError("{} is not a valid email".format(email))


def check_sha224_hash(password):
    if isinstance(password, str) and len(password) == 56:
        return password
    raise ValueError("Invalid password - expecting SHA224")


def check_user_attr(user_attr):
    return {
        "email": str(check_valid_email(user_attr.get("email", None))),
        "name": str(user_attr.get("name", "")),
        "username": str(user_attr.get("name", "")),
        "password": str(check_sha224_hash(user_attr.get("password"))),
        "id": str(user_attr.get("id", "")),
    }


def create_user(user_attr, db_session=None):
    db_session = verify_db_session(db_session)
    for key in user_attr:
        user_attr[key] = str(user_attr[key])
    user = UserDb(**user_attr)
    print("> dbmodel.create_user")
    print("{")
    for key, value in user_attr.items():
        print("  '%s': '%s' (%s)," % (key, value, type(value)))
    print("}")
    db_session.add(user)
    db_session.commit()
    return parse_user(user)


def make_user_query(db_session=None, **kwargs):
    print("> dbmodel.make_user_query")
    print("{")
    for key, value in kwargs.items():
        print("  '%s': '%s' (%s)," % (key, value, type(value)))
    print("}")
    db_session = verify_db_session(db_session)
    kwargs = filter_dict_for_none(kwargs)
    query = db_session.query(UserDb).filter_by(**kwargs)
    print(
        "> dbmodel.maker_user_query count=%s, query=\n====\n%s\n===="
        % (query.count(), query)
    )
    return query


def load_user(db_session=None, **kwargs):
    query = make_user_query(db_session=db_session, **kwargs)
    return query.one()


def load_users():
    return make_user_query().all()


def update_user_from_attr(user_attr, db_session=None):
    db_session = verify_db_session(db_session)
    user = load_user(id=user_attr["id"])
    for key, value in user_attr.items():
        if value is not None:
            if key == "password":
                user.set_password(value)
            else:
                setattr(user, key, value)
    db_session.add(user)
    db_session.commit()
    return parse_user(user)


def delete_user(user_id, db_session=None):
    db_session = verify_db_session(db_session)
    user = load_user(id=user_id)
    user_attr = parse_user(user)
    query = make_custom_query(user_id=user_id, db_session=db_session)
    for record in query.all():
        db_session.delete(record)
    db_session.delete(user)
    db_session.commit()
    return user_attr


def get_user_server_dir(dirpath, user_id=None):
    """
    Returns a user directory if user_id is defined
    """
    try:
        if not is_current_user_anonymous():
            current_user_id = user_id if user_id else current_user.id
            user_path = os.path.join(dirpath, str(current_user_id))
            if not (os.path.exists(user_path)):
                os.makedirs(user_path)
            return user_path
    except:
        return dirpath
    return dirpath


# OBJECT functions


def make_custom_query(user_id=None, custom_type="project", db_session=None, **kwargs):
    db_session = verify_db_session(db_session)
    kwargs = filter_dict_for_none(kwargs)
    if user_id is not None:
        kwargs["user_id"] = user_id
    if custom_type is not None:
        kwargs["custom_type"] = custom_type
    return db_session.query(CustomDb).filter_by(**kwargs)


def load_custom_attr(custom_id, custom_type="project", db_session=None):
    query = make_custom_query(
        id=custom_id, custom_type=custom_type, db_session=db_session
    )
    return query.one().attr


def load_custom_records(user_id=None, custom_type="project", db_session=None):
    query = make_custom_query(
        user_id=user_id, custom_type=custom_type, db_session=db_session
    )
    return query.all()


def load_custom_attr_list(user_id=None, custom_type="project", db_session=None):
    records = load_custom_records(
        user_id=user_id, custom_type=custom_type, db_session=db_session
    )
    return [record.attr for record in records]


def create_custom_id(db_session=None, **kwargs):
    db_session = verify_db_session(db_session)
    record = CustomDb(**kwargs)
    db_session.add(record)
    db_session.commit()
    return record.id


def save_custom(custom_id, custom_type, byte_str, attr, db_session=None):
    db_session = verify_db_session(db_session)
    record = make_custom_query(
        id=custom_id, custom_type=custom_type, db_session=db_session
    ).one()
    record.blob = byte_str
    attr = copy.deepcopy(attr)
    attr["userId"] = str(record.user_id)
    attr["modifiedTime"] = repr(arrow.now().format())
    record.attr = attr
    db_session.add(record)
    db_session.commit()


def get_user_id_of_custom(custom_id, db_session=None):
    record = make_custom_query(id=custom_id, db_session=db_session).one()
    return record.user_id


def load_custom_byte_str(obj_id, custom_type, db_session=None):
    record = make_custom_query(
        id=obj_id, custom_type=custom_type, db_session=db_session
    ).one()
    return record.blob


def delete_custom(custom_id, db_session=None):
    db_session = verify_db_session(db_session)
    record = make_custom_query(id=custom_id, db_session=db_session).one()
    db_session.delete(record)
    db_session.commit()
