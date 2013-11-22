import user_controller
import child_group_controller

from google.appengine.api import xmpp
from google.appengine.api import app_identity


class ChatController:

    @staticmethod
    def sendToAllUsers(sender, content):
        content = sender.split('@')[0] + ": " + content
        users = user_controller.UserController.getAllUsers()
        for user in users:
            xmpp.send_message(user.email, content)

    @staticmethod
    def sendToAllGroups(sender, content):
        content = sender.split('@')[0] + ": " + content
        content = app_identity.get_application_id() + ":" + content
        groups = child_group_controller.ChildGroupController.getAllChildGroups()
        for group in groups:
            xmpp.send_message(group.email, content)

