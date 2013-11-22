import config

from google.appengine.ext import ndb


class ChildGroup(ndb.Model):
    email = ndb.StringProperty(required=True)
    added_at = ndb.DateTimeProperty(auto_now_add=True)


def findChildGroup(email):
    q = ChildGroup.query(ChildGroup.email == email)
    return q.get()


def haveSameChildGroup(email):
    q = ChildGroup.query(ChildGroup.email == email)
    if q.count() > 0:
        return True
    else:
        return False


def getAllChildGroups():
    return ChildGroup.query().fetch()


def addFatherGroup(email):
    if config.FATHER_GROUP_EMAIL != "":
        return False

    config.FATHER_GROUP_EMAIL = email
    return True


def delFatherGroup():
    config.FATHER_GROUP_EMAIL = ""


def addChildGroup(email):
    if haveSameChildGroup(email):
        return False

    group = ChildGroup(email=email)
    group.put()

    return True


def delChildGroup(email):
    if not haveSameChildGroup(email):
        return False

    group = findChildGroup(email)
    group.key.delete()

    return True
