def require_privilege(operation, resource, template_403_name=None):
    def decorator(function):
        function.required_privilege = {
            'operation': operation,
            'resource': resource,
            'template_403_name': template_403_name,
        }
        return function
    return decorator
