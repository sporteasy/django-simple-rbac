from django.views.generic import TemplateView
from acl.decorators import require_privilege
from acl.views import AclViewMixin


class ListPostView(AclViewMixin, TemplateView):
    template_name = 'list.html'


class ViewPostView(AclViewMixin, TemplateView):
    template_name = 'view.html'


class UpdatePostView(AclViewMixin, TemplateView):
    template_name = 'update.html'


class DeletePostView(AclViewMixin, TemplateView):
    template_name = 'delete.html'


list_post_view = require_privilege('list', 'post')(ListPostView.as_view())
view_post_view = require_privilege('view', 'post')(ViewPostView.as_view())
update_post_view = require_privilege('update', 'post')(UpdatePostView.as_view())
delete_post_view = require_privilege('delete', 'post')(DeletePostView.as_view())
