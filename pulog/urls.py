import os
from django.contrib import admin
from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.conf import settings
from pulog.models import Post, Category
from pulog.feed import LatestPosts
admin.autodiscover()

post_info = {
    'queryset': Post.objects.get_post(),
}

feed = {
    'latest': LatestPosts,
}

urlpatterns = patterns('',
        (r'^admin/(.*)', admin.site.root),
        (r'^feed/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', 
            {'feed_dict': feed}),
#        (r'^templates/(?P<path>.*)$', 'django.views.static.serve',
#            {'document_root': settings.TEMPLATE_ROOT}),
#        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#            {'document_root': MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'pulog.media_serve.serve', 
            {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += patterns('pulog.views.utils',
    (r'^upload/$', 'upload'),
)

urlpatterns += patterns('pulog.views',
    (r'^$', 'index'),
    (r'^archives/$', 'index'),
    url(r'^archives/(?P<post_id>\d+).html$', 'single_post', name = 'post-single'),
    url(r'^archives/category/(?P<slugname>[^/]+)/$', 'category_view', name = 'post-category'),
    (r'^archives/category/(?P<slugname>[^/]+)/page/(?P<page_num>\d+)/$', 
        'category_view'),
    (r'^archives/(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'archive_view'),
    (r'^archives/(?P<year>\d{4})/(?P<month>[^/]+)/page/(?P<page_num>\d+)/$',
        'archive_view'),
    (r'^page/(?P<num>\d+)/$', 'page'),
    (r'^([-\w]+)/$', 'static_pages'),
#   (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page_num>\d+)$', 'archive_view'),
)

urlpatterns += patterns('pulog.views',
    url(r'^comment/post/$',          'comment.post_comment',       name='comment-post-comment'),
    url(r'^comment/posted/$',        'comment.comment_done',       name='comment-comment-done'),
    url(r'^comment/flag/(\d+)/$',    'moderation.flag',             name='comment-flag'),
    url(r'^comment/flagged/$',       'moderation.flag_done',        name='comment-flag-done'),
    url(r'^comment/delete/(\d+)/$',  'moderation.delete',           name='comment-delete'),
    url(r'^comment/deleted/$',       'moderation.delete_done',      name='comment-delete-done'),
    url(r'^comment/moderate/$',      'moderation.moderation_queue', name='comment-moderation-queue'),
    url(r'^comment/approve/(\d+)/$', 'moderation.approve',          name='comment-approve'),
    url(r'^comment/approved/$',      'moderation.approve_done',     name='comment-approve-done'),
)
