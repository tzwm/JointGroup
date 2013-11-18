import user_controller
import chat_controller

import webapp2
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.ext.webapp.util import run_wsgi_app


class XMPPHandler(xmpp_handlers.CommandHandler):

    def text_message(self, message=None):
        message = xmpp.Message(self.request.POST)
        sender = message.sender.split('/')[0]

        user_controller.UserController().addUser(sender)

        chat_controller.ChatController().sendToAll(sender, message.body)

    def test_command(self, message=None):
        message.reply("greate.")


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
