from django.conf.urls import url
from pages.blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    # админка
    url(r'^list/(?P<username>.+)/$', BlogListView.as_view(), name='blog_list'), # (?P<username>.+)
    url(r'^detail/(?P<pk>[0-9]+)/$', BlogDetailView.as_view(), name='blog_detail'),
    url(r'^create/$', BlogCreateView.as_view(), name='blog_create'),
    url(r'^update/(?P<pk>[0-9]+)/$', BlogUpdateView.as_view(), name='blog_update'),
    url(r'^delete/(?P<pk>[0-9]+)/$', BlogDeleteView.as_view(), name='blog_delete'),
]