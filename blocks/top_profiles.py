from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User


class TopProfilesMixin(ContextMixin):
    """
    Самые популярные анкеты
    """
    def get_context_data(self, **kwargs):
        context = super(TopProfilesMixin, self).get_context_data(**kwargs)
        context['top_users'] = User.objects.filter(is_active=True).order_by('-profile__viewed')[:10]
        return context