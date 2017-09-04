from django.db import models
from dry_library.backend.thumbnails import CreateThumbnail
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


class KindAnimal(CreateThumbnail, models.Model):
    """
    Справочник видов животных
    """
    kind = models.CharField(max_length=250, blank=False, null=False, verbose_name=_('Kind animal (dog, cat...)'))

    class Meta:
        verbose_name = _('Kind animal')
        verbose_name_plural = _('Kinds animals')

    def __str__(self):
        return self.kind


class KindAnimalAttr(models.Model):
    """
    Справочник характеристик видов животных
    """
    kind = models.ForeignKey(KindAnimal, on_delete=models.CASCADE, related_name='attrs', verbose_name=_('Kind animal'))
    attr = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Name attr(weight, color...)'))

    class Meta:
        verbose_name = _('Kind attribute')
        verbose_name_plural = _('Kind attributes')

    def __str__(self):
        return self.attr


class Animal(CreateThumbnail, models.Model):
    """
    Модель животного
    """
    user = models.ForeignKey(User, related_name='animals', on_delete=models.CASCADE, verbose_name=_('Owner'))
    first_name = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Name'))
    second_name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Nickname'))
    GENDER_CHOICES = (
        ('B', _('Boy')),
        ('G', _('Girl')),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=True, verbose_name=_('Gender'))
    info = models.TextField(blank=True, null=True, verbose_name=_('About animal'))
    birthday = models.DateField(blank=True, null=True, verbose_name=_('Birthday'))
    kind = models.ForeignKey(KindAnimal, related_name='animals', verbose_name=_('Kind animal'))
    avatar = models.ImageField(max_length=100, upload_to='animal/avatar', blank=True, null=True,
                               verbose_name=_('Avatar'))
    avatar_thumb = models.ImageField(max_length=100, upload_to='animal/avatar/thumbnail', blank=True, null=True)

    class Meta:
        verbose_name = _('Animal')
        verbose_name_plural = _('Animals')

    def __str__(self):
        return self.user.username + ' ' + self.first_name

    def save(self, *args, **kwargs):
        """
        Сохранение фото
        """
        try:
            this_record = Animal.objects.get(pk=self.pk)
            if this_record.avatar != self.avatar:
                this_record.avatar.delete(save=False)
                this_record.avatar_thumb.delete(save=False)
        except:
            pass

        self.create_thumbnail(width=100, height=100, from_img=self.avatar, to_img=self.avatar_thumb)

        force_update = False

        if self.id:
            force_update = True

        super(Animal, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Удаление фото
        """
        self.avatar.delete(save=False)
        self.avatar_thumb.delete(save=False)
        super(Animal, self).delete(*args, **kwargs)


class AnimalAttr(models.Model):
    """
    Характеристики животного
    """
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='attr', verbose_name=_('Animal'))
    kind = models.ForeignKey(KindAnimal, verbose_name=_('Kind animal'))
    attr = models.ForeignKey(KindAnimalAttr, verbose_name=_('Attributes'))
    value = models.CharField(max_length=50, blank=False, null=False, verbose_name=_('Value attribute'))

    class Meta:
        verbose_name = _('Animal attribute')
        verbose_name_plural = _('Animal attributes')

    def __str__(self):
        return self.animal.first_name + self.attr.attr + self.value