from django.views.generic.base import ContextMixin
from refdata.models import Banner
from random import randint


class BannerMixin(ContextMixin):
    """
    Примись баннера
    """
    def get_context_data(self, **kwargs):
        context = super(BannerMixin, self).get_context_data(**kwargs)
        active_banners = Banner.objects.filter(status=True)
        if active_banners:
            count = len(active_banners)
            random_index = randint(0, count-1)
            context['banner'] = active_banners[random_index].content
        return context