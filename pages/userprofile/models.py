from django.db import models

# сигналы
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from dry_library.backend.thumbnails import CreateThumbnail

from django.utils.translation import ugettext_lazy as _


class ProfileHobby(models.Model):
    """
    Интересы пользователя
    """
    name = models.CharField(max_length=50, blank=False, verbose_name=_('Hobby name'))

    class Meta:
        verbose_name = _('Hobby')
        verbose_name_plural = _('Hobbies')

    def __str__(self):
        return self.name


class Profile(CreateThumbnail, models.Model):
    """
    Модель расширяющая стандартную User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('User'))
    GENDER_CHOICES = (
        ('M', _('Men')),
        ('W', _('Woman')),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True, verbose_name=_('Gender'))
    phone = models.CharField(max_length=30, blank=True, null=True, verbose_name=_('Phone'))
    info = models.TextField(blank=True, null=True, verbose_name=_('About me'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    avatar = models.ImageField(max_length=100, upload_to='profile/avatar', blank=True, null=True,
                               verbose_name=_('Avatar'))
    avatar_thumb = models.ImageField(max_length=100, upload_to='profile/avatar/thumbnail', blank=True, null=True)
    hobbies = models.ManyToManyField(ProfileHobby, blank=True, verbose_name=_('Hobbies'))
    viewed = models.PositiveIntegerField(default=0, verbose_name=_('Viewed'))
    last_visit = models.DateTimeField(blank=True, null=True, verbose_name=_('Last date of visit'))
    vk = models.URLField(max_length=100, blank=True, null=True, verbose_name=_('Vkontakte'))
    ok = models.URLField(max_length=100, blank=True, null=True, verbose_name=_('Odnoklassniki'))
    fb = models.URLField(max_length=100, blank=True, null=True, verbose_name=_('Facebook'))
    insta = models.URLField(max_length=100, blank=True, null=True, verbose_name=_('Instagram'))

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = Profile.objects.get(pk=self.pk)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
                this_record.avatar_thumb.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=100, height=100, from_img=self.avatar, to_img=self.avatar_thumb)

        force_update = False

        if self.id:
            force_update = True

        super(Profile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.avatar.delete(save=False)
        self.avatar_thumb.delete(save=False)
        super(Profile, self).delete(*args, **kwargs)


class ProfileImages(CreateThumbnail, models.Model):
    """
    Изображения пользователя
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', verbose_name=_('User'))
    image = models.ImageField(max_length=100, upload_to='profile/images', blank=False, null=False,
                              verbose_name=_('Photo'))
    image_thumb = models.ImageField(max_length=100, upload_to='profile/images/thumbnail', blank=False, null=False,)
    date = models.DateTimeField(auto_now_add=True, blank=False, null=False, verbose_name=_('Date added'))
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name=_('Description'))

    class Meta:
        ordering = ['-date']
        verbose_name = _('Profile image')
        verbose_name_plural = _('Profile images ')

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = ProfileImages.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
                this_record.image_thumb.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=100, height=100, from_img=self.image, to_img=self.image_thumb)

        force_update = False

        if self.id:
            force_update = True
        super(ProfileImages, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.image.delete(save=False)
        self.image_thumb.delete(save=False)
        super(ProfileImages, self).delete(*args, **kwargs)


class ProfileAbout(models.Model):
    """
    Информация о пользователе
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='about', blank=False, verbose_name=_('User'))
    FIND_CHOICES = (
        ('M', _('Men')),
        ('W', _('Woman')),
    )
    find = models.CharField(max_length=2, choices=FIND_CHOICES, blank=True, verbose_name=_('I find'))
    GOAL_CHOICES = (
        ('CMN', _('Communicate')),
        ('FNF', _('Find new friends')),
        ('GOD', _('Go on a date')),
    )
    purpose = models.CharField(max_length=3, choices=GOAL_CHOICES, blank=True, verbose_name=_('Purpose of dating'))
    about_me = models.TextField(blank=True, verbose_name=_('About me'))

    class Meta:
        verbose_name = _('Profile About')
        verbose_name_plural = _('Profiles About')



class ProfileViewed(models.Model):
    """
    Модель для учета уникальных просмотров профиля пользователя
    """
    profile_page = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_viewed', blank=False,
                                     verbose_name=_('Profile_page'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_viewed', blank=False,
                             verbose_name=_('User'))

    class Meta:
        verbose_name = _('Profile Viewed')
        verbose_name_plural = _('Profiles Vieweds')

    def __str__(self):
        return '[' + self.profile_page.username + '] - ' + self.user.username
