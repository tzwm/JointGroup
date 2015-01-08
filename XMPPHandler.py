# -*- coding: utf-8 -*-

import user_controller
import chat_controller
import group_controller
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
        chat_controller.sendToAllChildGroups(sender, message.body)

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
        groups = group_controller.getAllChildGroups()
        lists = ""
        for group in groups:
            lists = lists + group.email + '\n'

        message.reply(lists)

    def displayGroupName_command(self, message=None):
        content = group_controller.getGroupName()
        message.reply(content)

    def setGroupName_command(self, message=None):
        content = message.body.split('/setGroupName')[1]
        content = content.strip()
        group_controller.setGroupName(content)

    def displayFatherGroup_command(self, message=None):
        if group_controller.FatherGroup.query().count() > 0:
            message.reply(group_controller.FatherGroup.query().get())
        else:
            message.reply("No Father Group.")

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
        if not group_controller.addFatherGroup(content):
            message.reply("Sorry. This group already had the father group.")
            return False
        else:
            message.reply("To add father group successfully.")

        myEmail = app_identity.get_application_id() + "@appspot.com"
        xmpp.send_message(content, '/addChildGroupBot '+ myEmail)
        return True

    def delFatherGroup_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isRootUser(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = group_controller.delFatherGroup()
        if not content:
            message.reply("Sorry. This group didn't have father group.")
            return False
        else:
            message.reply("Deleted successfully.")

        myEmail = app_identity.get_application_id() + "@appspot.com"
        xmpp.send_message(content, '/delChildGroupBot '+ myEmail)
        return True

    def addChildGroupBot_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isBot(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/addChildGroupBot')[1].strip()
        group_controller.addChildGroup(content)
        return True

    def delChildGroupBot_command(self, message=None):
        sender = message.sender.split('/')[0]
        if not user_controller.isBot(sender):
            message.reply("Sorry. Permission denied.")
            return False

        content = message.body.split('/delChildGroupBot')[1].strip()
        group_controller.delChildGroup(content)
        return True

    def toGroup_command(self, message=None):
        content = message.body.split('/toGroup')[1].strip()
        sender = message.sender.split('/')[0]
        sender = sender.split('@')[0]
        receiver = content.split(' ')[0]
        content = group_controller.getGroupName() + '-' + sender + ':' + content.split(' ')[1]
        xmpp.send_message(receiver, content)

    def help_command(self, message=None):
        message.reply(config.HELP_MANUAL)
