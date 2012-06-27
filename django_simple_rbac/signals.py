from django.dispatch import Signal


filter_authorities = Signal(providing_args=['authorities', 'request', 'operation', 'resource'])
