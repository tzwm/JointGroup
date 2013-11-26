# -*- coding: utf-8 -*-

import user_controller
import group_controller

from google.appengine.api import xmpp
from google.appengine.api import app_identity
from google.appengine.ext import ndb


def sendToAllUsers(sender, content):
    if not sender.split('@')[1] == "appspot.com":
        content = sender.split('@')[0] + ": " + content

    users = user_controller.getAllUsers()
    for user in users:
        if user.email == sender:
            continue
        xmpp.send_message(user.email, content)


def sendToAllChildGroups(sender, content):
    if sender.split('@')[1].strip() == "appspot.com":
        content = group_controller.getGroupName() + '-' + content
    else:
        content = group_controller.getGroupName() + '-' + sender.split('@')[0] + ": " + content

    #content = group_controller.getGroupName() + '-' + content

    groups = group_controller.getAllChildGroups()
    for group in groups:
        xmpp.send_message(group.email, content)

