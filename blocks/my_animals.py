from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User
from pages.animal.models import Animal


class MyAnimalsMixin(ContextMixin):
    """
    Вывод животных пользователя
    """
    def get_context_data(self, **kwargs):
        context = super(MyAnimalsMixin, self).get_context_data(**kwargs)
        try:
            cur_user = User.objects.get(username=self.request.user.username)
        except:
            pass
        else:
            context['animals'] = Animal.objects.filter(user=cur_user)
        return context