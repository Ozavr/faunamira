from django.views.generic.base import ContextMixin
from pages.blog.views import Blog


class LatestArticlesMixin(ContextMixin):
    """
    Последние записи в блоге
    """
    def get_context_data(self, **kwargs):
        context = super(LatestArticlesMixin, self).get_context_data(**kwargs)
        articles = Blog.objects.filter(user__is_active=True).order_by('-date')[:4]
        context['latest_articles'] = articles
        return context