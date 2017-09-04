from django.template.context_processors import csrf
from django.template import loader
from django.http import JsonResponse, Http404

from django.contrib.auth.models import User
from .forms import ProfileAboutForm

from dry_library.backend.similar_people import get_similar_people


def get_about_edit_form(request):
    """
    Получение формы редактирования информации о себе
    """
    if request.is_ajax():
        form = ProfileAboutForm(instance=request.user.about)
        context = {
            'form': form
        }
        context.update(csrf(request))
        html_content = loader.render_to_string(template_name='include/edit_profile_about.html', context=context)
        data = {
            'html_content': html_content
        }
        return JsonResponse(data)
    else:
        return Http404

def post_about_edit_form(request):
    """
    Изменение информации пользователя о нем
    """
    if request.is_ajax():
        form = ProfileAboutForm(data=request.POST, instance=request.user.about)
        if form.is_valid():
            form.save()
            data = {'reload': True}
            return JsonResponse(data)
        context = {
            'form': form,
        }
        context.update(csrf(request))
        html_content = loader.render_to_string(template_name='include/edit_profile_about.html', context=context)
        data = {
            'html_content': html_content,
            'reload': False
        }
        return JsonResponse(data)
    else:
        return Http404


def similar_people(request):
    """
    Получение списка похожих пользователей
    """
    if request.is_ajax():
        username = request.POST.get('username')
        try:
            people = User.objects.get(username=username)
        except:
            pass
        else:
            results = get_similar_people(people=people, user=request.user)[:25]
            context = {
                'similar_people': results
            }
            context.update(csrf(request))
            html_content = loader.render_to_string(template_name='include/similar_people.html', context=context)
            data = {
                'html_content': html_content
            }
            return JsonResponse(data)
    else:
        return Http404