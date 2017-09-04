from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from pages.animal.views import AnimalView, AnimalCreateView, AnimalUpdateView, AnimalDeleteView, AttrCreateView, \
    AttrUpdateView, AttrDeleteView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/', AnimalView.as_view(), name='animal'),
    url(r'^create/$', AnimalCreateView.as_view(), name='animal_create'),
    url(r'^update/(?P<pk>[0-9]+)/', AnimalUpdateView.as_view(), name='animal_update'),
    url(r'^delete/(?P<pk>[0-9]+)/', AnimalDeleteView.as_view(), name='animal_delete'),
    url(r'^addattr/(?P<pk>[0-9]+)/', AttrCreateView.as_view(), name='attr_create'),
    url(r'^updattr/(?P<pk>[0-9]+)/', AttrUpdateView.as_view(), name='attr_update'),
    url(r'^delattr/(?P<pk>[0-9]+)/', AttrDeleteView.as_view(), name='attr_delete'),
]