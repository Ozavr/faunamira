from django.contrib import admin
from django.contrib.auth.models import User
from pages.userprofile.models import Profile, ProfileImages, ProfileHobby, ProfileAbout
from pages.animal.models import Animal


class ProfileInline(admin.StackedInline):
    """
    Вкладка: Профиль пользователя
    """
    model = Profile
    fields = ('gender', 'phone', 'info', 'birthday', 'avatar', 'hobbies', 'viewed', 'last_visit',
              'vk', 'ok', 'fb', 'insta')
    readonly_fields = ('viewed', 'last_visit')

class ProfileAboutInline(admin.StackedInline):
    """
    Вкладка о пользователе
    """
    model = ProfileAbout
    fields = ('find', 'purpose', 'about_me')

class ProfileImagesInline(admin.TabularInline):
    """
    Вкладка: Изображения пользователя
    """
    model = ProfileImages
    fields = ('image', 'date', 'description')
    readonly_fields = ('date',)


class AnimalInline(admin.StackedInline):
    model = Animal
    fields = ('first_name', 'second_name', 'gender', 'info', 'birthday', 'kind', 'avatar')


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline, ProfileAboutInline, ProfileImagesInline, AnimalInline, ]
    list_display = ['username', 'first_name', 'last_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(ProfileHobby)