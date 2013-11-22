import user_controller
import chat_controller
import child_group_controller
import config

import webapp2
from google.appengine.api import xmpp
from google.appengine.ext.webapp import xmpp_handlers
from google.appengine.api import urlfetch
from google.appengine.api import app_identity


class XMPPHandler(xmpp_handlers.CommandHandler):

    def text_message(self, message=None):
        message = xmpp.Message(self.request.POST)
        sender = message.sender.split('/')[0]

        user_controller.addUser(sender)

        chat_controller.sendToAllUsers(sender, message.body)
        chat_controller.sendToAllGroups(sender, message.body)

        xmpp.send_message('tzwmtest2@apspot.com', 'ok')

    def test_command(self, message=None):
        url = "http://" + app_identity.get_default_version_hostname() + "/getXML"
        #url = "http://tzwmtest3.appspot.com/getXML"
        result = urlfetch.fetch(url, deadline=5)
        if result.status_code == 200:
            message.reply(result.content)

    def list_command(self, message=None):
        users = user_controller.getAllUsers()
        lists = ""
        for user in users:
            lists = lists + user.email + '\n'
            message.reply(lists)

    def listChildGroup_command(self, message=None):
        groups = child_group_controller.getAllChildGroups()
        lists = ""
        for group in groups:
            lists = lists + group.email + '\n'
            message.reply(lists)

    def displayFatherGroup_command(self, message=None):
        if config.FATHER_GROUP_EMAIL != "":
            message.reply(config.FATHER_GROUP_EMAIL)
        else:
            message.reply("No fathre group.")

    def displayRoot_command(self, message=None):
        if config.ROOT_EMAIL != "":
            message.reply(config.ROOT_EMAIL)
        else:
            message.reply("No Root.")

    def delUser_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isRootUser(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/delUser')[1]
        content = content.strip()
        if user_controller.delUser(content):
            message.reply("Deleted successfully.")
        else:
            message.reply("Delete failed.")

    def addFatherGroup_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isRootUser(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/addFatherGroup')[1].strip()
        if not child_group_controller.addFatherGroup(content):
            message.reply("Sorry. This group already had the father group.")
            return False
        else:
            message.reply("To add father group successfully.")

        myEmail = app_identity.get_application_id() + "@appspot.com"
        xmpp.send_message(content, '/addChildGroup '+ myEmail)
        return True

    def addChildGroup_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isBot(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/addChildGroup')[1].strip()
        child_group_controller.addChildGroup(content)
        return True
