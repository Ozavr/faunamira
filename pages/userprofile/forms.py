from django.forms import ModelForm
from allauth.account.forms import ChangePasswordForm
from django.contrib.auth.models import User
from pages.userprofile.models import Profile, ProfileImages, ProfileAbout


class ProfileAboutForm(ModelForm):
    """
    Форма на странице пользователя 'Обо мне'
    """
    class Meta:
        model = ProfileAbout
        fields = ('find', 'purpose', 'about_me')


class UserForm(ModelForm):
    """
    Форма для редактирования основной информации пользователя
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileForm(ModelForm):
    """
    Форма для редактирования дополнительной информации пользователя
    """
    class Meta:
        model = Profile
        fields = ('gender', 'phone', 'info', 'birthday', 'avatar', 'vk', 'ok', 'fb', 'insta')


class PasswordChangeForm(ChangePasswordForm):
    """
    Форма для смены пароля
    """
    class Meta:
        model = User
        fields = ('oldpassword', 'password1', 'password2')


class ProfileImageForm(ModelForm):
    """
    Форма загрузки фотографии
    """
    class Meta:
        model = ProfileImages
        fields = ('image', 'description')