import config

from google.appengine.ext import ndb


class ChildGroup(ndb.Model):
    email = ndb.StringProperty(required=True)
    added_at = ndb.DateTimeProperty(auto_now_add=True)

class ChildGroupController:

    @staticmethod
    def getAllChildGroups():
        return ChildGroup.query().fetch()

    @staticmethod
    def addFatherGroup(email):
        if config.FATHER_GROUP_EMAIL!="":
            return False

        config.FATHER_GROUP_EMAIL = email
        return True

    @staticmethod
    def delFatherGroup():
        config.FATHER_GROUP_EMAIL = ""

    @staticmethod
    def addChildGroup(email):
        if ChildGroupController.haveSameChildGroup(email):
            return False

        group = ChildGroup(email=email)
        group.put()

        return True

    @staticmethod
    def delChildGroup(email):
        if not ChildGroupController.haveSameChildGroup(email):
            return False

        group = ChildGroupController.findChildGroup(email)
        group.key.delete()

        return True

    @staticmethod
    def findChildGroup(email):
        q = ChildGroup.query(ChildGroup.email == email)
        return q.get()

    @staticmethod
    def haveSameChildGroup(email):
        q = ChildGroup.query(ChildGroup.email == email)
        if q.count() > 0:
            return True
        else:
            return False

