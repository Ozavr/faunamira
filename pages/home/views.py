from django.views.generic import TemplateView
from django.utils.timezone import now
from django.template import loader
from django.http import JsonResponse
from datetime import date

from pages.animal.models import Animal
from pages.userprofile.models import Profile

from blocks.user import AuthFormMixin
from blocks.my_animals import MyAnimalsMixin
from blocks.panel_filters import FiltersMixin
from blocks.banner import BannerMixin
from blocks.random_profiles import RandomProfilesMixin
from blocks.top_profiles import TopProfilesMixin
from blocks.latest_articles import LatestArticlesMixin
from blocks.footer import FooterMixin


class HomeView(FiltersMixin, BannerMixin, RandomProfilesMixin, TopProfilesMixin, MyAnimalsMixin, LatestArticlesMixin,
               FooterMixin, TemplateView, AuthFormMixin):
    template_name = 'home.html'


def get_animal_results(request):
    """
    Получение результатов поиска по животным
    """
    if request.is_ajax:
        kind = request.POST.get('kind')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        query = Animal.objects.all()
        compl = True                            # статус поиска

        if kind:
            new_query = query.filter(kind=kind)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if gender:
            new_query = query.filter(gender=gender)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if age:
            age = int(age)
            cur_date = now().date()
            max_date = date(cur_date.year - age, cur_date.month, cur_date.day)
            min_date = date(cur_date.year - age - 1, cur_date.month, cur_date.day)
            new_query = query.filter(birthday__lte=max_date, birthday__gt=min_date)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False

        context = {
            'animal_results': query,
            'compl': compl,
        }
        html_content = loader.render_to_string(template_name='include/results.html', context=context)

        data = {
            'html_content': html_content,
        }
        return JsonResponse(data)


def get_people_results(request):
    """
    Получение результатов поиска по людям
    """
    if request.is_ajax:
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        hobbies = request.POST.getlist('hobbies[]')

        query = Profile.objects.filter(user__is_active=True)
        compl = True

        if gender:
            new_query = query.filter(gender=gender)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False
        if age:
            age = int(age)
            cur_date = now().date()
            max_date = date(cur_date.year - age, cur_date.month, cur_date.day)
            min_date = date(cur_date.year - age - 1, cur_date.month, cur_date.day)
            new_query = query.filter(birthday__lte=max_date, birthday__gt=min_date)
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False

        if hobbies:
            new_query = query.filter(hobbies__in=hobbies).distinct()
            if new_query:
                query = new_query
                if compl != False:
                    compl = True
            else:
                compl = False

        context = {
            'compl': compl,
            'people_results': query,
        }

        html_content = loader.render_to_string(template_name='include/results.html', context=context)

        data = {
            'html_content': html_content,
        }
        return JsonResponse(data)