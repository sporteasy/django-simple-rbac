from django.dispatch import Signal


# args=['authorities', 'request', 'operation', 'resource']
filter_authorities = Signal()
