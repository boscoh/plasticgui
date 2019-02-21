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
import os
import time

from flask import session
from flask_login import current_app, current_user, login_user, logout_user

from . import dbmodel


# User handlers

def adminGetUsers():
    return {
        'users': map(dbmodel.parse_user, dbmodel.load_users())
    }


def publicRegisterUser(user_attr):
    username = dbmodel.check_user_attr(user_attr)['username']

    try:
        dbmodel.load_user(username=username)
        raise Exception("User already exists")
    except:

        print("> handler.publicRegisterUser user_attr", user_attr)

        created_user_attr = dbmodel.create_user(user_attr)
        return {
            'success': True,
            'user': created_user_attr
        }


def publicGetCurrentUser():
    return dbmodel.parse_user(current_user)


def loginUpdateUser(user_attr):
    return {
        'success': True,
        'user': dbmodel.update_user_from_attr(user_attr)
    }


def publicLoginUser(user_attr):
    if not dbmodel.is_current_user_anonymous():
        print("> handler.publicLoginUser already logged-in")
        return {
            'success': True,
            'user': dbmodel.parse_user(current_user)
        }

    user_attr = dbmodel.check_user_attr(user_attr)
    kwargs = {}
    if user_attr['username']:
        kwargs['username'] = user_attr['username']
    if user_attr['email']:
        kwargs['email'] = user_attr['email']

    print("> handler.publicLoginUser loading", kwargs, user_attr)
    try:
        user = dbmodel.load_user(**kwargs)
    except:
        raise Exception("User not found")

    if user.check_password(user_attr['password']):
        login_user(user)
        return {
            'success': True,
            'user': dbmodel.parse_user(user)
        }

    raise Exception("User/Password does not match")


def adminDeleteUser(user_id):
    username = dbmodel.delete_user(user_id)['username']
    print("> handler.admin_delete_user ", username)
    return adminGetUsers()


def publicLogoutUser():
    logout_user()
    session.clear()
    return {'success': True}


# model handlers

this_dir = os.path.dirname(__file__)


def publicGetText():
    return {
        "text": "Example text from server",
        "isRunning": True
    }


def publicDownloadGetReadme():
    return {
        "filename": os.path.join(this_dir, "../../readme.md"),
        "data": {"success": True}
    }


def publicDownloadLogo():
    return {
        "filename": os.path.join(this_dir, "../../client/static/logo.png"),
        "data": {"success": True}
    }


def publicUploadFiles(files):
    timestamp = str(int(time.time()))
    timestamp_dir = os.path.join(current_app.config['SAVE_FOLDER'], timestamp)
    if not os.path.isdir(timestamp_dir):
        os.makedirs(timestamp_dir)
    urls = []
    new_filenames = []
    for file in files:
        basename = os.path.basename(file)
        new_filename = os.path.join(timestamp_dir, basename)
        urls.append(os.path.join('/file', timestamp, basename))
        new_filenames.append(new_filename)
        os.rename(file, new_filename)
    print('> handler.publicUploadFiles', new_filenames)
    return {'files': urls}


def publicPushTask():
    records = dbmodel.load_obj_records(obj_type="task")
    if len(records) == 0:
        dbmodel.create_obj_id(attr={"n": 1}, obj_type="task")
        records = dbmodel.load_obj_records(obj_type="task")
    record = records[0]
    record.attr["n"] += 1
    dbmodel.save_object(record.id, record.obj_type, "", record.attr)
    return {"attr": record.attr}
