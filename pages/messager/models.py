from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Dialog(models.Model):
    """
    Модель диалоги
    """
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs_from',
                                  verbose_name=_('User from'))
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs_to',
                                  verbose_name=_('User to'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Dialog')
        verbose_name_plural = _('Dialogs')
        ordering = ['-date']

    def __str__(self):
        return self.user_from.username + ' - ' + self.user_to.username


class Message(models.Model):
    """
    Модель сообщение
    """
    dialog = models.ForeignKey(Dialog, related_name='messages', on_delete=models.CASCADE, verbose_name=_('Dialog'))
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sended_messages',
                                  verbose_name=_('User from'))
    message = models.TextField(verbose_name=_('Message'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-date']

    def __str__(self):
        return self.user_from.username + ' - ' + self.date
