import copy
import rbac.acl
import yaml
from django.conf import settings


STRATEGY_FILTER = 'filter'
STRATEGY_DIRECT_DENY = 'deny'
registries = {}


def load_registry_from_yaml(filename):
    with file(filename, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        registry = rbac.acl.Registry()

        # load roles
        try:
            for role in config['roles']:
                parents = role.get('parents', [])
                registry.add_role(role['name'], parents)
        except (KeyError, TypeError):
            pass

        # load resources
        try:
            for resource in config['resources']:
                parents = resource.get('parents', [])
                registry.add_resource(resource['name'], parents)
        except (KeyError, TypeError):
            pass

        # load rules
        try:
            for rule in config['rules']:
                try:
                    for resource in rule['resources']:
                        for role in rule['roles']:
                            for operation in rule['operations']:
                                assertion = None
                                if 'assertion' in rule:
                                    [module_name, function_name] = rule['assertion'].rsplit('.', 1)
                                    _module = __import__(module_name, globals(), locals(), [function_name], -1)
                                    assertion = getattr(_module, function_name)
                                args = (role, operation, resource, assertion)
                                if rule['type'] == 'allow':
                                    registry.allow(*args)
                                else:
                                    registry.deny(*args)
                except (KeyError, TypeError):
                    pass
        except (KeyError, TypeError):
            pass

    return registry


def _get_roles_from_authority(authority, request):
    """
    Returns a list of roles for the given request, in the given authority context.
    Roles are cached in the request object for improved performance.
    """
    if not hasattr(request, '_cached_rbac_roles'):
        request._cached_rbac_roles = {}
    try:
        authority_key = (authority.acl_registry_name, authority.id)
    except:
        authority_key = (authority.acl_registry_name,)
    if not authority_key in request._cached_rbac_roles:
        request._cached_rbac_roles[authority_key] = authority.get_acl_roles(request) or []  # get roles from authority
    return request._cached_rbac_roles[authority_key]


def _get_acl_registry(authority, request):
    try:
        registry = copy.deepcopy(registries[authority.acl_registry_name])
        roles =_get_roles_from_authority(authority, request)
        # dynamically add a special __current__ role
        registry[0].add_role('__current__', parents=roles)
        return registry
    except Exception as e:
        return None, False, False


class Adapter(object):

    def __init__(self, adaptee):
        self.adaptee = adaptee

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(other) == str(self)


class ResourceAdapter(Adapter):

    def __str__(self):
        return self.adaptee if isinstance(self.adaptee, basestring) else self.adaptee.acl_resource_name

    @property
    def acl_authorities(self):
        try:
            return self.adaptee.acl_authorities
        except AttributeError:
            return []


class CurrentRoleAdapter(Adapter):
    def __str__(self):
        return '__current__'


class Permission(object):
    def __init__(self, granted=False, authority=None):
        self.granted = granted
        self.authority = authority

    def __nonzero__(self):
        return bool(self.granted)


# load registries
authorities = getattr(settings, 'ACL_AUTHORITIES', {})
for (name, file_, direct_allow, direct_deny) in authorities:
    registries[name] = (load_registry_from_yaml(file_), direct_allow, direct_deny)
