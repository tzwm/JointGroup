import debugger

import webapp2
from google.appengine.api import xmpp
from google.appengine.ext.webapp.util import run_wsgi_app

class XMPPHandler(webapp2.RequestHandler):
    def post(self):
        message = xmpp.Message(self.request.POST)
        message.reply(message.sender)

        currentUser = debugger.GroupUser()
        currentUser.user_email = message.sender
        currentUser.put()
        

#app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              #debug=True)

#def main():
    #run_wsgi_app(app)

#if __name__ == "__main__":
    #main()

