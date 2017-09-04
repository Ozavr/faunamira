from django.db import models
from tinymce import models as tinymce_models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User


class Blog(models.Model):
    """
    Блог
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog', verbose_name=_('Author'))
    title = models.CharField(max_length=100, blank=False, null=False, verbose_name=_('Title'))
    article = tinymce_models.HTMLField(blank=False, null=False, verbose_name=_('Content'))
    date = models.DateTimeField(blank=False, null=False, verbose_name=_('Date of publication'))

    class Meta:
        ordering = ['-date']
        verbose_name = _('Blog')
        verbose_name_plural = _('Blog')

    def __str__(self):
        return (self.user.username) + ' ' + self.title

    def get_actual_articles(articles):
        act_articles = articles.filter(date__lte=timezone.now())
        return act_articles

