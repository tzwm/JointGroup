import users_manager

import webapp2
from google.appengine.api import xmpp
from google.appengine.ext.webapp.util import run_wsgi_app


class XMPPHandler(webapp2.RequestHandler):

    def post(self):
        message = xmpp.Message(self.request.POST)
        sender = message.sender.split('/')
        sender = sender[0]

        userManager = users_manager.UsersManager()
        userManager.addUser(sender)

        users = userManager.getAllUsers()
        for user in users:
            xmpp.send_message(user.email, message.body)


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
