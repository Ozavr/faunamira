from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify

from tinymce import models as tinymce_model


class Banner(models.Model):
    """
    Модель для баннера
    """
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Banner name'))
    content = tinymce_model.HTMLField(blank=False, verbose_name=_('Banner content'))
    status = models.BooleanField(default=False, verbose_name=_('Active status'))

    class Meta:
        verbose_name = _('Banner')
        verbose_name_plural = _('Banners')

    def __str__(self):
        return self.title


class AltMenu(models.Model):
    """
    Модель для альтернативного меню
    """
    title = models.CharField(max_length=30, blank=False, verbose_name=_('Title'))
    url = models.URLField(max_length=50, blank=False, verbose_name=_('Url'))
    order = models.PositiveIntegerField(blank=False, verbose_name=_('order'))
    slug = models.SlugField(max_length=30, blank=True, null=True, verbose_name=_('Slug'))

    class Meta:
        verbose_name = _('Alt menu')
        verbose_name_plural = _('Alt menu')
        ordering = ['order']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Создание slug из title
        """
        self.slug = slugify(self.title)
        super(AltMenu, self).save(*args, **kwargs)


class SocialLink(models.Model):
    """
    Ссылки на социальные сети
    """
    TYPES = (                           # Варианты социальных сетей
        ('vk', _('Vkontakte')),
        ('ok', _('Odnoklassniki')),
        ('fb', _('Facebook')),
        ('in', _('Instagram')),
    )
    title = models.CharField(max_length=2, choices=TYPES, blank=False, verbose_name=_('Title'))
    url = models.URLField(max_length=50, blank=False, verbose_name=_('Url'))

    class Meta:
        verbose_name = _('Social link')
        verbose_name_plural = _('Social links')

    def __str__(self):
        return self.title


