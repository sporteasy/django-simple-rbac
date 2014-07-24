from django.template.response import TemplateResponse
from .helpers import is_allowed, Http403Exception
from .utils import get_class


class ACLMiddleware(object):

    def _create_403_response(self, request, operation, resource, authority=None, template_name=None, message=None):
        template_name = template_name or '403.html'
        response = TemplateResponse(request, template_name, {
            'operation': operation,
            'resource': resource,
            'authority': authority,
            'message': message,
            'status_code': '403'
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

            # dynamically import the class to fetch the associated template_403_name
            view_class = get_class(view_func.__module__, view_func.__name__)
            template_name = getattr(view_class, 'template_403_name', None)

            # if specific authority template is defined, use it
            authorities_template_names = getattr(view_class, 'authorities_template_names', None)
            if authorities_template_names:
                template_name = authorities_template_names.get(granted.authority, template_name)

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

            # if specific authority template is defined, use it
            if hasattr(exception.view, 'authorities_template_names'):
                if hasattr(exception, 'authority') and exception.view.authorities_template_names.get(exception.authority):
                    kwargs['template_name'] = exception.view.authorities_template_names.get(exception.authority)

        if hasattr(exception, 'authority'):
            kwargs['authority'] = exception.authority
        return self._create_403_response(request, exception.operation, exception.resource,
                                         message=exception.message, **kwargs)
