from django.template.response import TemplateResponse
from .helpers import is_allowed, Http403Exception


class ACLMiddleware(object):

    def _create_403_response(self, request, operation, resource, authority=None, template_name=None):
        template_name = template_name or '403.html'
        response = TemplateResponse(request, template_name, {
            'operation': operation,
            'resource': resource,
            'authority': authority
        })
        response.status_code = 403
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if (hasattr(view_func, 'required_privilege')):

            # check privilege, return None if allowed
            privilege = view_func.required_privilege
            granted = is_allowed(request, privilege['operation'], privilege['resource'])
            if granted:
                return None

            # tricky hack to retrieve original view class
            view_class = view_func.func_closure[1].cell_contents
            template_name = getattr(view_class, 'template_403_name', None)

            # Finally deny access. We have to return a response here because any raised exception wouldn't be caught
            # by process_exception method (it catches exceptions only when they are raised by a view)
            return self._create_403_response(request, privilege['operation'], privilege['resource'],
                authority=granted.authority, template_name=template_name)

    def process_exception(self, request, exception):
        """
        Called when an exception is raised by a view.
        """
        if not isinstance(exception, Http403Exception):
            return None

        kwargs = {}
        if hasattr(exception, 'view'):
            if hasattr(exception.view, 'template_403_name'):
                kwargs['template_name'] = exception.view.template_403_name
        if hasattr(exception, 'authority'):
            kwargs['authority'] = exception.authority
        return self._create_403_response(request, exception.operation, exception.resource, **kwargs)
