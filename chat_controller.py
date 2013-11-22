import user_controller
import child_group_controller

from google.appengine.api import xmpp
from google.appengine.api import app_identity


def sendToAllUsers(sender, content):
    if sender.split('@')[1] == "appspot.com":
        content = sender.split('@')[0] + '-' + content
    else:
        content = sender.split('@')[0] + ": " + content

    users = user_controller.getAllUsers()
    for user in users:
        xmpp.send_message(user.email, content)


def sendToAllGroups(sender, content):
    content = sender.split('@')[0] + ": " + content
    groups = child_group_controller.getAllChildGroups()
    for group in groups:
        xmpp.send_message(group.email, content)
