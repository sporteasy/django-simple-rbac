def require_privilege(operation, resource):
    def decorator(function):
        function.required_privilege = {
            'operation': operation,
            'resource': resource
        }
        return function
    return decorator
