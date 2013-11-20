import user_controller
import chat_controller
import group_controller

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
        message.reply("great.")

    def list_command(self, message=None):
        users = user_controller.UserController.getAllUsers()
        lists = ""
        for user in users:
            lists = lists + user.email + '\n'
        message.reply(lists)

    def delUser_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.UserController.isRootUser(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/delUser')[1]
        content = content.strip()
        if user_controller.UserController.delUser(content):
            message.reply("Deleted successfully.")
        else:
            message.reply("Delete failed.")

    def addGroup_command(self, message=None):
        content = message.body.split('/addGroup')[1].strip()
        group_controller.GroupController.addGroup(content)


app = webapp2.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                              debug=True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
