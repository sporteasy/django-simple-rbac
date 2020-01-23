from builtins import str
def if_not_admin(registry, role, operation, resource):
    return str(resource) != "admin"
