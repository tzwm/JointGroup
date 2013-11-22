import user_controller
import chat_controller
import child_group_controller

import webapp2
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.api import urlfetch
from google.appengine.api import app_identity


class XMPPHandler(xmpp_handlers.CommandHandler):

    def text_message(self, message=None):
        message = xmpp.Message(self.request.POST)
        sender = message.sender.split('/')[0]

        user_controller.UserController().addUser(sender)

        chat_controller.ChatController().sendToAllUsers(sender, message.body)
        chat_controller.ChatController().sendToAllGroups(sender, message.body)

    def test_command(self, message=None):
        url = "http://" + app_identity.get_default_version_hostname() + "/getXML"
        #url = "http://tzwmtest3.appspot.com/getXML"
        result = urlfetch.fetch(url, deadline=5)
        if result.status_code == 200:
            message.reply(result.content)

    def test1_command(self, message=None):
        xmpp.send_message('tzwmtest@appspot.com', '/test2')

    def test2_command(self, message=None):
        message.reply('ok')

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

    def addFatherGroup_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.UserController.isRootUser(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/addFatherGroup')[1].strip()
        if not child_group_controller.ChildGroupController.addFatherGroup(content):
            message.reply("Sorry. This group already had the father group.")
            return False
        else:
            message.reply("To add father group successfully.")

        myEmail = app_identity.get_application_id() + "@appspot.com"
        xmpp.send_message(content, '/addChildGroup '+ myEmail)
        return True

    def addChildGroup_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.UserController.isBot(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/addChildGroup')[1].strip()
        child_group_controller.ChildGroupController.addChildGroup(content)
        return True
