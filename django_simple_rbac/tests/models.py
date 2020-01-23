from builtins import object
from ..registry import Adapter


class Member(object):
    acl_resource_name = 'member'
    acl_role_name = 'member'

    def __init__(self, name):
        self.name = name


class Moderator(Member):
    acl_resource_name = 'moderator'
    acl_role_name = 'moderator'


class Admin(Moderator):
    acl_resource_name = 'admin'
    acl_role_name = 'admin'


class ResourceAdapter(Adapter):
    def __str__(self):
        return self.adaptee.acl_resource_name


class RoleAdapter(Adapter):
    def __str__(self):
        return self.adaptee.acl_role_name
