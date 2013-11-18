from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()
    created_at = ndb.DateTimeProperty(auto_now_add=True)


class UsersManager:

    def getAllUsers(self):
        return User.query().fetch()

    def addUser(self, email):
        if self.haveSameUser(email):
            return False

        user = User()
        user.email = email
        user.put()

        return True

    def haveSameUser(self, email):
        q = User.query(User.email == email)
        if q.count() > 0:
            return True
        else:
            return False
