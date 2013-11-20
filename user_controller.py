import config
from google.appengine.ext import ndb


class User(ndb.Model):
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    is_admin = ndb.BooleanProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class UserController:

    @staticmethod
    def getAllUsers():
        return User.query().fetch()

    @staticmethod
    def addUser(email):
        if UserController.haveSameUser(email):
            return False


        user = User()
        user.email = email
        user.username = email.split('@')[0]
        user.is_admin = False
        if UserController.isRootUser(email):
            user.is_admin = True
        user.put()

        return True

    @staticmethod
    def delUser(email):
        if not UserController.haveSameUser(email):
            return False

        user = UserController.findUser(email)
        user.key.delete()

        return True

    @staticmethod
    def changeUsername(email, username):
        user = UserController.findUser(email)
        user.username = username
        user.put()

    @staticmethod
    def addAdmin(email):
        user = UserController.findUser(email)
        user.is_admin = True
        user.put()

    @staticmethod
    def haveSameUser(email):
        q = User.query(User.email == email)
        if q.count() > 0:
            return True
        else:
            return False

    @staticmethod
    def findUser(email):
        q = User.query(User.email == email)
        return q.get()

    @staticmethod
    def isRootUser(email):
        return config.ROOT_EMAIL == email

