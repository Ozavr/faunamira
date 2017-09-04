from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User


class RandomProfilesMixin(ContextMixin):
    """
    Случайные анкеты пользователей
    """
    def get_context_data(self, **kwargs):
        context = super(RandomProfilesMixin, self).get_context_data(**kwargs)
        users = User.objects.filter(is_active=True).order_by('?')[:14]
        context['random_users'] = users
        return context