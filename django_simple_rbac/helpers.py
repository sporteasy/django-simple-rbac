from builtins import str
from .registry import _get_acl_registry, ResourceAdapter, CurrentRoleAdapter, Permission
from .signals import filter_authorities


def is_allowed(request, operation, resource, authorities=None):
    # wrap resource
    wrapped_resource = resource if isinstance(resource, ResourceAdapter) else ResourceAdapter(resource)

    if authorities:
        return _is_allowed(request, operation, wrapped_resource, authorities)

    if not hasattr(request, '_cached_permissions'):
        request._cached_permissions = {}

    key = "::".join([str(operation), str(resource)])
    if key not in request._cached_permissions:
        request._cached_permissions[key] = _is_allowed(request, operation, wrapped_resource)
    return request._cached_permissions[key]


def _is_allowed(request, operation, resource, authorities=None):
    """
    is_allowed(request, 'update', resource_instance)
    is_allowed(request, 'update', 'resource_name')
    is_allowed(request, 'update', resource_instance, authorities)
    """

    # we have no predefined authorities (which is the most common case)
    if not authorities:
        try:
            authorities = list(resource.acl_authorities)
        except AttributeError as e:
            authorities = []

    # apply filters on authority list
    filter_authorities.send(sender=None, authorities=authorities, request=request, operation=operation, resource=resource)

    # the request is wrapped and become the special '__current__' role
    current_role = CurrentRoleAdapter(request)

    # check permissions on each authority
    for authority in authorities:
        registry, direct_allow, direct_deny = _get_acl_registry(authority, request)
        if registry:
            try:
                if registry.is_allowed(current_role, operation, resource):
                    if direct_allow:
                        return Permission(True, authority.acl_registry_name)
                elif direct_deny:
                    return Permission(False, authority.acl_registry_name)
            except Exception as e:
                # the resource is probably unknown by this registry, but it would be nice
                # to have information about it in a debug panel.
                pass

    # is we reach this point, permission is denied
    return Permission(False)


class Http403Exception(Exception):
    def __init__(self, operation, resource, view=None, authority=None, message=None, *args, **kwargs):
        super(Http403Exception, self).__init__(*args, **kwargs)
        self.operation = operation
        self.resource = resource
        self.message = message
        if view:
            self.view = view
        if authority:
            self.authority = authority
