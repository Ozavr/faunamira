from django.views.generic import TemplateView, UpdateView, CreateView, DeleteView
from allauth.account.views import PasswordChangeView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from pages.userprofile.models import ProfileImages, ProfileViewed, ProfileAbout
from pages.userprofile.forms import PasswordChangeForm
from pages.userprofile.forms import UserForm, ProfileForm, ProfileImageForm, ProfileAboutForm
from pages.blog.models import Blog

from blocks.my_animals import MyAnimalsMixin
from blocks.user import AuthFormMixin
from blocks.banner import BannerMixin
from blocks.footer import FooterMixin

from dry_library.backend.similar_people import get_similar_people


class ProfileView(MyAnimalsMixin, BannerMixin, FooterMixin, CreateView, AuthFormMixin):
    """
    Представление для профиля пользователя
    """
    model = User
    template_name = 'profile.html'
    form_class = ProfileAboutForm

    def get_people(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get(self, request, *args, **kwargs):
        people = self.get_people()
        user = request.user
        if user.is_authenticated and people != user:
            prof_view = ProfileViewed.objects.filter(profile_page=people, user=user)
            if not prof_view:
                people.profile.viewed += 1
                people.profile.save()
                pr_vi = ProfileViewed(profile_page=people, user=user)
                pr_vi.save()
        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Показ профиля пользователя по username
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        people = self.get_people()
        if people.is_active:

            # данные пользователя
            context['people'] = people
            context['images'] = ProfileImages.objects.filter(user=people)

            # последние статьи пользователя
            context['latest_user_articles'] = Blog.objects.filter(user=people).order_by('-date')[:4]

            # обо мне
            try:
                about = ProfileAbout.objects.get(user__username=people.username)
            except:
                context['form'] = self.get_form()
            else:
                context['about'] = about

            # похожие анкеты
            context['similar_people'] = get_similar_people(user=self.request.user, people=people)[:5]

            # статистика
            context['stat_viewed'] = people.profile.viewed
            context['stat_animals'] = people.animals.count()
            context['stat_blog'] = people.blog.count()
            context['stat_visit'] = people.profile.last_visit

        return context

    def form_valid(self, form):
        user = self.request.user
        obj = form.save(commit=False)
        obj.user = user
        return super(ProfileView, self).form_valid(form)

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.get_people().username})


class ProfileUpdateView(UpdateView):
    """
    Редактирование профиля пользователя
    """
    template_name = 'profile_update.html'
    form_class = UserForm
    profile_form_class = ProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        cur_user = self.get_object()
        people = get_object_or_404(User, username=kwargs.get('username'))
        if cur_user:
            if cur_user == people:
                return super(ProfileUpdateView, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        profile = self.request.user.profile
        context['profile_form'] = self.profile_form_class(instance=profile)
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        userform = self.form_class(request.POST, instance=self.object)
        proform = self.profile_form_class(request.POST, request.FILES, instance=self.object.profile)
        if userform.is_valid() and proform.is_valid():
            userdata = userform.save(commit=False)
            userdata.save()
            profdata = proform.save(commit=False)
            profdata.user = userdata
            profdata.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(context={'form': userform, 'profile_form': proform})

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'username': self.request.user.username})


class ProfileChangePassword(PasswordChangeView):
    """
    Смена пароля пользователя
    """
    template_name = 'profile_password_change.html'
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(User, username=kwargs.get('username'))
        if profile.is_active and (user == profile):
            return super(ProfileChangePassword, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.kwargs.get('username')})


class ProfileDelete(TemplateView):
    """
    Удаление пользователя
    """
    model = User
    template_name = 'profile_delete.html'

    def get(self, request, *args, **kwargs):
        cur_user = request.user
        people = get_object_or_404(User, username=kwargs.get('username'))
        if cur_user:
            if cur_user == people:
                return super(ProfileDelete, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(ProfileDelete, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=request.user.username)
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('user_delete_success', kwargs={'username': user.username}))


class ProfileDeleteSuccess(TemplateView):
    """
    Успешное удаление пользователя
    """
    model = User
    template_name = 'profile_delete_success.html'

    def get(self, request, *args, **kwargs):
        cur_user = request.user
        people = get_object_or_404(User, username=kwargs.get('username'))
        if cur_user:
            if cur_user == people:
                return super(ProfileDeleteSuccess, self).get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(ProfileDeleteSuccess, self).get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, username=kwargs.get('username'))
        return context


class ProfileImageAdd(CreateView):
    """
    Добавление изображения
    """
    model = ProfileImages
    template_name = 'profile_image_add.html'
    form_class = ProfileImageForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super(ProfileImageAdd, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.request.user.username})

    def form_valid(self, form):
        user = self.request.user
        obj = form.save(commit=False)
        obj.user = user
        return super(ProfileImageAdd, self).form_valid(form)


class ProfileImageUpdate(UpdateView):
    """
    Редактирование изображения и его информации
    """
    model = ProfileImages
    template_name = 'profile_image_update.html'
    form_class = ProfileImageForm

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        people = get_object_or_404(ProfileImages, pk=kwargs.get('pk')).user
        user = request.user
        if people.is_active and (people == user):
            return super(ProfileImageUpdate, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))


class ProfileImageDelete(DeleteView):
    """
    Удаление изображений
    """
    model = ProfileImages
    template_name = 'profile_image_delete.html'

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        people = get_object_or_404(ProfileImages, pk=kwargs.get('pk')).user
        user = request.user
        if people.is_active and (people == user):
            return super(ProfileImageDelete, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))



