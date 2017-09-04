from django.conf.urls import url

from pages.messager.views import DialogsView, MessagesView


urlpatterns = [
    url(r'^$', DialogsView.as_view(), name='dialogs'),
    url(r'^(?P<pk>[0-9]+)/$', MessagesView.as_view(), name='message'),
]