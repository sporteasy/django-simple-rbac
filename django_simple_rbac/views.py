from .helpers import is_allowed, Http403Exception


class AclViewMixin(object):
    template_403_name = '403.html'

    def check_privilege(self, request, operation, resource, authorities=None):
        granted = is_allowed(request, operation, resource, authorities)
        if not granted:
            raise Http403Exception(operation, resource, view=self, authority=granted.authority)
