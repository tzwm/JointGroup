from google.appengine.ext import ndb


class Group(ndb.Model):
    groupname = ndb.StringProperty()
    email = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class GroupController:

    @staticmethod
    def getAllGroups():
        return Group.query().fetch()

    @staticmethod
    def addGroup(email):
        if GroupController.haveSameGroup(email):
            return False

        group = Group()
        group.email = email
        group.groupname = email.split('@')[0]
        group.put()

        return True

    @staticmethod
    def delGroup(email):
        if not GroupController.haveSameGroup(email):
            return False

        group = GroupController.findGroup(email)
        group.key.delete()

        return True

    @staticmethod
    def findGroup(email):
        q = Group.query(Group.email == email)
        return q.get()

    @staticmethod
    def haveSameGroup(email):
        q = Group.query(Group.email == email)
        if q.count() > 0:
            return True
        else:
            return False
