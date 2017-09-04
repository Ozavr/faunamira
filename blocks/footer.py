from django.views.generic.base import ContextMixin
from refdata.models import AltMenu, SocialLink


class FooterMixin:
    """
    Футер сайта
    """
    def get_context_data(self, **kwargs):
        context = super(FooterMixin, self).get_context_data(**kwargs)
        context['alt_menu'] = AltMenu.objects.all()
        link_vk = SocialLink.objects.get(title='vk')
        link_ok = SocialLink.objects.get(title='ok')
        link_fb = SocialLink.objects.get(title='fb')
        link_in = SocialLink.objects.get(title='in')
        if link_vk:
            context['link_vk'] = link_vk
        if link_ok:
            context['link_ok'] = link_ok
        if link_fb:
            context['link_fb'] = link_fb
        if link_in:
            context['link_in'] = link_in
        return context