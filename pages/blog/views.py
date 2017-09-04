from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from blocks.user import AuthFormMixin

from django.contrib.auth.models import User
from pages.blog.models import Blog

from pages.blog.forms import BlogForm


class BlogListView(AuthFormMixin, ListView):
    """
    Блог пользователя
    """
    template_name = 'blog_list.html'
    context_object_name = 'blog_list'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        people = get_object_or_404(User, username=kwargs.get('username'))
        if people.is_active:
            return super(BlogListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        people = get_object_or_404(User, username=self.kwargs.get('username'))
        context['people'] = people
        context['blog_list'] = self.get_queryset()
        return context

    def get_queryset(self):
        people = get_object_or_404(User, username=self.kwargs.get('username'))
        articles = Blog.objects.filter(user=people)
        act_articles = Blog.get_actual_articles(articles=articles)
        return act_articles


class BlogDetailView(TemplateView, AuthFormMixin):
    """
    Статья
    """
    model = Blog
    template_name = 'blog_detail.html'


    def get(self, request, *args, **kwargs):
        author = get_object_or_404(Blog, pk=kwargs.get('pk')).user
        if author.is_active:
            return super(BlogDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Blog, pk=kwargs.get('pk'))
        return context



class BlogCreateView(CreateView):
    """
    Создание статьи
    """
    template_name = 'blog_create.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user and user.is_active:
            return super(BlogCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        return super(BlogCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})


class BlogUpdateView(UpdateView):
    """
    Редактирование статьи
    """
    template_name = 'blog_update.html'
    model = Blog
    form_class = BlogForm

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            self.form = BlogForm(instance=self.obj)
            return super(BlogUpdateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse_lazy('blog_detail', kwargs={'pk': self.object.id})

class BlogDeleteView(DeleteView):
    """
    Удаление статьи
    """
    template_name = 'blog_delete.html'
    model = Blog

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Blog, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            return super(BlogDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(BlogDeleteView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        return context

    def get_success_url(self):
        return reverse_lazy('blog_list', kwargs={'username': self.request.user})