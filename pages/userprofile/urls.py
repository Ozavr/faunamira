from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from pages.userprofile.views import ProfileView, ProfileUpdateView, ProfileChangePassword, \
    ProfileDelete, ProfileDeleteSuccess, ProfileImageAdd, ProfileImageDelete, ProfileImageUpdate
from pages.userprofile.async import get_about_edit_form, post_about_edit_form, similar_people

urlpatterns = [
    # аккаунт
    url(r'^user/(?P<username>.+)/', ProfileView.as_view(), name='user'),

    # функции для ajax
    url(r'^get_edit_about/$', get_about_edit_form, name='about_edit'),    # редактирование Обо мне
    url(r'^post_edit_about/$', post_about_edit_form, name='about_edit'),
    url(r'^get_similar_people/$', similar_people, name='similar_people'),   # похожие анкеты "Показать еще"

    # редактирование аккаунта
    url(r'^update/(?P<username>.+)/$', ProfileUpdateView.as_view(), name='user_update'),
    url(r'^password/(?P<username>.+)/$', ProfileChangePassword.as_view(), name='user_password'),
    url(r'^delete/(?P<username>.+)/$', ProfileDelete.as_view(), name='user_delete'),
    url(r'^delete_success/(?P<username>.+)/$', ProfileDeleteSuccess.as_view(), name='user_delete_success'),

    # фото пользователя
    url(r'addphoto/$', ProfileImageAdd.as_view(), name='user_image_add'),
    url(r'updphoto/(?P<pk>[0-9]+)/$', ProfileImageUpdate.as_view(), name='user_image_upd'),
    url(r'delphoto/(?P<pk>[0-9]+)/$', ProfileImageDelete.as_view(), name='user_image_del'),
]
