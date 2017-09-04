from django.views.generic.base import ContextMixin
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader

from allauth.account.forms import LoginForm, SignupForm


class AuthFormMixin(ContextMixin):
    """
    Добавление в контекст форм аутентификации
    """
    def get_context_data(self, **kwargs):
        context = {}
        if not self.request.user.is_authenticated:
            context['login_form'] = LoginForm
            context['signup_form'] = SignupForm
        return context


def user_login(request):
    """
    Функция авторизации по ajax
    """
    if request.is_ajax:
        login_form = LoginForm(request.POST)
        login = request.POST.get('login')
        password = request.POST.get('password')
        if login_form.is_valid():
            user = auth.authenticate(username=login, password=password)
            if user and user.is_active:
                auth.login(request, user)
                data = {
                    'reload': True
                }
                return JsonResponse(data)

        context = {
            'reload': False,
            'login_form': login_form,
            'signup_form': SignupForm,
        }
        context.update(csrf(request))
        html_content = loader.render_to_string(template_name='include/user/user.html', context=context)
        data = {
            'html_content': html_content
        }
        return JsonResponse(data)
    else:
        return Http404


def user_signup(request):
    """
    Функция авторизации по ajax
    """
    if request.is_ajax:
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            signup_form.save(request)
            data = {
                'reload': True
            }
            return JsonResponse(data)

        context = {
            'reload': False,
            'login_form': LoginForm,
            'signup_form': signup_form
            }
        context.update(csrf(request))
        html_content = loader.render_to_string(template_name='include/user/user.html', context=context)
        data = {
            'html_content': html_content
        }
        return JsonResponse(data)
    else:
        return Http404