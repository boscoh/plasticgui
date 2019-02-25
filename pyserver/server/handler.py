"""
handler.py
=========

RPC-JSON API Web-handlers

To use define functions with name
- public* public handlers
- login* requires login first
- admin* requires admin login

All handlers must return a JSON dictionary, except for downloadable functions
Handlers can take parameters, which are expected to be only JSON-compatible
Python data structures.
"""

from __future__ import print_function
from __future__ import unicode_literals
import os
import time
import smtplib
import uuid
import datetime
import six
import pprint

from flask import session, current_app, request
from flask_login import current_user, login_user, logout_user

from . import dbmodel


# User handlers


def adminGetUsers():
    return {"users": list(map(dbmodel.parse_user, dbmodel.load_users()))}


def publicRegisterUser(user_attr):
    user_attr = dbmodel.check_user_attr(user_attr)
    print("publicRegisterUser\n" + pprint.pformat(user_attr, indent=2))

    errors = []
    if not user_attr.get("name"):
        errors.append("no user name")
    if not user_attr.get("email"):
        errors.append("no email")
    if not user_attr.get("password"):
        errors.append("no Password")

    if len(errors) > 0:
        raise Exception(", ".join(errors))

    try:
        user = dbmodel.load_user(email=user_attr["email"])
    except:
        user = None
    if user:
        raise Exception("User already exists")

    created_user_attr = dbmodel.create_user(user_attr)
    return {"success": True, "user": created_user_attr}


def publicGetCurrentUser():
    return dbmodel.parse_user(current_user)


def loginUpdateUser(user_attr):
    user_attr = dbmodel.check_user_attr(user_attr)
    return {"success": True, "user": dbmodel.update_user_from_attr(user_attr)}


def publicLoginUser(user_attr):
    if not dbmodel.is_current_user_anonymous():
        print("> handler.publicLoginUser already logged-in")
        return {"success": True, "user": dbmodel.parse_user(current_user)}

    user_attr = dbmodel.check_user_attr(user_attr)

    print("> handler.publicLoginUser\n" + pprint.pformat(user_attr, indent=2))
    try:
        user = dbmodel.load_user(email=user_attr["email"])
    except:
        raise Exception("User not found")

    if user.check_password(user_attr["password"]):
        login_user(user)
        return {"success": True, "user": dbmodel.parse_user(user)}

    raise Exception("User/Password does not match")


def adminDeleteUser(user_id):
    username = dbmodel.delete_user(user_id)["username"]
    print("> handler.admin_delete_user ", username)
    return adminGetUsers()


def publicLogoutUser():
    logout_user()
    session.clear()
    return {"success": True}


def publicForgotPassword(email):
    email = str(email)
    user = dbmodel.load_user(email=email)
    if not user:
        raise Exception("No user found with email: " + email)

    token = str(uuid.uuid4().hex)
    smtp_server = current_app.config["SMTP_SERVER"]
    smtp_port = current_app.config["SMTP_PORT"]
    sender_email = current_app.config["SMTP_EMAIL"]
    password = current_app.config["SMTP_PASSWORD"]
    client_url = request.environ["HTTP_ORIGIN"]

    user.reset_password_token = token
    expire_time = datetime.datetime.now() + datetime.timedelta(hours=5)
    user.reset_password_expires_on = expire_time
    db_session = dbmodel.verify_db_session()
    db_session.add(user)
    db_session.commit()

    msg = (
        "From: onewordname@yahoo.com\n"
        + "To: %s\n" % email
        + "Subject: Password Reset\n"
        + "You are receiving this because you (or someone else) "
        + "have requested the reset of the password for your account.\n"
        + "\n"
        + "Please click on the following link, or paste this "
        + "into your browser to complete the process:\n"
        + "\n"
        + "%s/#/reset-password/%s\n" % (client_url, token)
        + "\n"
        + "If you did not request this, please ignore this email"
        + "and your password will remain unchanged.\n"
    )

    # Try to log in to server and send email
    try:
        print("> handler.publicForgotPassword %s\n----\n%s\n---" % (email, msg))
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, password)
        server.sendmail(sender_email, email, msg)
        print("> handler.publicForgotPassword success")
        server.quit()
        return {
            "success": True,
            "message": "An e-mail has been sent to "
            + email
            + " with further instructions.",
        }
    except Exception as e:
        raise Exception("publicForgotPassword fail email send %s" % e)


def publicResetPassword(token, password):
    token = str(token)
    password = str(password)
    user = dbmodel.load_user(reset_password_token=token)
    is_found = False
    now = datetime.datetime.now()
    if user:
        print("> handler.publicForgotPassword times")
        print("  now:", now)
        print("  expire:", user.reset_password_expires_on)
        if now < user.reset_password_expires_on:
            is_found = True
    if not is_found:
        raise Exception("Password reset token is invalid or has expired.")

    try:
        user.reset_password_expires_on = None
        user.reset_password_token = None
        user.set_password(password)
        db_session = dbmodel.verify_db_session()
        db_session.add(user)
        db_session.commit()
        return {"success": True}
    except Exception as e:
        raise Exception("Update failure %s" % e)


# model handlers

this_dir = os.path.dirname(__file__)


def publicGetText():
    return {"text": "Example text from server", "isRunning": True}


def publicDownloadGetReadme():
    return {
        "filename": os.path.join(this_dir, "../../readme.md"),
        "data": {"success": True},
    }


def publicDownloadLogo():
    return {
        "filename": os.path.join(this_dir, "../../client/static/logo.png"),
        "data": {"success": True},
    }


def publicUploadFiles(files):
    timestamp = str(int(time.time()))
    timestamp_dir = os.path.join(current_app.config["SAVE_FOLDER"], timestamp)
    if not os.path.isdir(timestamp_dir):
        os.makedirs(timestamp_dir)
    urls = []
    new_filenames = []
    for file in files:
        basename = os.path.basename(file)
        new_filename = os.path.join(timestamp_dir, basename)
        urls.append(os.path.join("/file", timestamp, basename))
        new_filenames.append(new_filename)
        os.rename(file, new_filename)
    print("> handler.publicUploadFiles", new_filenames)
    return {"files": urls}


def publicPushTask():
    records = dbmodel.load_custom_records(custom_type="task")
    if len(records) == 0:
        dbmodel.create_custom_id(attr={"n": 1}, custom_type="task")
        records = dbmodel.load_custom_records(custom_type="task")
    record = records[0]
    record.attr["n"] += 1
    dbmodel.save_custom(record.id, record.custom_type, six.b(""), record.attr)
    return {"attr": record.attr}
