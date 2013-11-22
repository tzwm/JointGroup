from google.appengine.ext import ndb
from google.appengine.api import app_identity


class FatherGroup(ndb.Model):
    email = ndb.StringProperty(required=True)
    added_at = ndb.DateTimeProperty(auto_now_add=True)


class ChildGroup(ndb.Model):
    email = ndb.StringProperty(required=True)
    added_at = ndb.DateTimeProperty(auto_now_add=True)


def findChildGroup(email):
    q = ChildGroup.query(ChildGroup.email == email)
    return q.get()


def findFatherGroup(email):
    q = FatherGroup.query(FatherGroup.email == email)
    return q.get()


def haveSameChildGroup(email):
    q = ChildGroup.query(ChildGroup.email == email)
    if q.count() > 0:
        return True
    else:
        return False


def haveFatherGroup(email):
    if email.split('@')[0] == app_identity.get_application_id():
        return True

    q = FatherGroup.query(FatherGroup.email == email)
    if q.count() > 0:
        return True
    else:
        return False


def getAllChildGroups():
    return ChildGroup.query().fetch()


def getFatherGroup():
    return FatherGroup.query().fetch()


def addFatherGroup(email):
    if haveFatherGroup(email):
        return False

    father = FatherGroup(email=email)
    father.put()
    return True


def delFatherGroup():
    if not haveFatherGroup(email):
        return False

    father = findFatherGroup(email)
    father.key.delete()
    return True

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
