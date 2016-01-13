from importlib import import_module


def get_class(module_name, cls_name):
    try:
        module = import_module(module_name)
    except ImportError:
        raise ImportError('Invalid class path: {}'.format(module_name))
    try:
        cls = getattr(module, cls_name)
    except AttributeError:
        raise ImportError('Invalid class name: {}'.format(cls_name))
    else:
        return cls
