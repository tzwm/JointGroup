import user_controller

from google.appengine.api import xmpp


class ChatController:

    @staticmethod
    def sendToAll(sender, content):
        content = sender.split('@')[0] + ": " + content

        users = user_controller.UserController.getAllUsers()
        for user in users:
            xmpp.send_message(user.email, content)
