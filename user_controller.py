# -*- coding: utf-8 -*-

import config
from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    is_admin = ndb.BooleanProperty(required=True, default=False)
    created_at = ndb.DateTimeProperty(auto_now_add=True)


def haveSameUser(email):
    q = User.query(User.email == email)
    if q.count() > 0:
        return True
    else:
        return False


def findUser(email):
    q = User.query(User.email == email)
    return q.get()


def isRootUser(email):
    return config.ROOT_EMAIL == email


def isBot(email):
    return not email.find('@appspot.com') == -1


def getAllUsers():
    return User.query().fetch()


def addUser(email):
    if haveSameUser(email):
        return False

    if isBot(email):
        return False

    user = User(email=email,
                username=email.split('@')[0])
    if isRootUser(email):
        user.is_admin = True
    user.put()

    return True


def delUser(email):
    if not haveSameUser(email):
        return False

    user = findUser(email)
    user.key.delete()

    return True


def changeUsername(email, username):
    user = findUser(email)
    user.username = username
    user.put()


def addAdmin(email):
    user = findUser(email)
    user.is_admin = True
    user.put()
