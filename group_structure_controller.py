import group_controller

from google.appengine.ext import ndb


class GroupStructure(ndb.Model):
    parent = ndb.StructuredProperty(group_controller.Group)
    children = ndb.StringProperty(group_controller.Group,
                                  repeated=True)


