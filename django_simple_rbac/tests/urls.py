from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^post/list$', 'someapp.views.list_post_view'),
    url(r'^post/view$', 'someapp.views.view_post_view'),
    url(r'^post/update$', 'someapp.views.update_post_view'),
    url(r'^post/delete$', 'someapp.views.delete_post_view'),
)
