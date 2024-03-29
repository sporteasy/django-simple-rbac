from builtins import str
from builtins import object
import copy
import rbac.acl
import yaml
from importlib import import_module
from django.conf import settings
from django.utils.functional import cached_property

STRATEGY_FILTER = 'filter'
STRATEGY_DIRECT_DENY = 'deny'
registries = {}


def load_registry_from_yaml(filename):
    with open(filename, "r") as f:
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
                                    module_name, function_name = rule['assertion'].rsplit('.', 1)
                                    _module = import_module(module_name)
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


def _get_authority_key(authority):
    try:
        return authority.acl_registry_name, authority.id
    except AttributeError:
        return authority.acl_registry_name


def _get_roles_from_authority(authority, request):
    """
    Returns a list of roles for the given request, in the given authority context.
    Roles are cached in the request object for improved performance.
    """
    if not hasattr(request, '_cached_rbac_roles'):
        request._cached_rbac_roles = {}

    authority_key = _get_authority_key(authority)

    if not authority_key in request._cached_rbac_roles:
        request._cached_rbac_roles[authority_key] = authority.get_acl_roles(request) or []  # get roles from authority

    return request._cached_rbac_roles[authority_key]


def _get_acl_registry(authority, request):
    """
    Returns the ACL registry for the given request, in the given authority context.
    Registries are cached in the request object for improved performance.
    """
    try:
        if not hasattr(request, '_cached_rbac_registries'):
            request._cached_rbac_registries = {}

        authority_key = _get_authority_key(authority)

        if not authority_key in request._cached_rbac_registries:
            registry = copy.deepcopy(registries[authority.acl_registry_name])
            roles =_get_roles_from_authority(authority, request)
            registry[0].add_role('__current__', parents=roles)  # dynamically add a special __current__ role
            request._cached_rbac_registries[authority_key] = registry

        return request._cached_rbac_registries[authority_key]
    except Exception as e:
        return None, False, False


class Adapter(object):

    def __init__(self, adaptee):
        try:
            self.adaptee = str(adaptee.strip())
        except AttributeError:
            self.adaptee = adaptee

    @cached_property
    def _hash(self):
        """We want to cache the hash because it won't change over time."""
        return hash(str(self))

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return str(other) == str(self)


class ResourceAdapter(Adapter):

    @cached_property
    def _str(self):
        """We want to cache this because it won't change over time."""
        try:
            return str(self.adaptee.acl_resource_name)
        except AttributeError:
            return self.adaptee

    def __str__(self):
        return self._str

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

    def __bool__(self):
        return bool(self.granted)


# load registries
authorities = getattr(settings, 'ACL_AUTHORITIES', {})
for (name, file_, direct_allow, direct_deny) in authorities:
    registries[name] = (load_registry_from_yaml(file_), direct_allow, direct_deny)
