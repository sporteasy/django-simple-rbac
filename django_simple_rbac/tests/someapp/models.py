from django.dispatch import receiver
from django_simple_rbac.signals import filter_authorities


class ForumAuthority(object):
    acl_registry_name = 'forum'

    def get_acl_roles(self, request):
        known_users = {
            'karl': ['member'],
            'simon': ['moderator'],
            'nizar': ['admin'],
            'albin': ['admin', 'owner']
        }

        if request.user.is_authenticated() and request.user.first_name in known_users:
            return known_users[request.user.first_name]

        return ['anonymous']


class Post(object):
    acl_authorities = [ForumAuthority()]
    def __init__(self):
        self.id = 42
        self.title = "This is the title"
        self.body = "This is the body"


@receiver(filter_authorities)
def on_filter_authorities(sender=None, authorities=None, request=None, operation=None, resource=None, **kwargs):
    if not len(authorities):
        authorities.append(ForumAuthority())
