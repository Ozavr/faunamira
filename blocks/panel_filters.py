from django.views.generic.edit import ContextMixin
from django.contrib.auth.models import User

from pages.animal.models import Animal
from pages.home.forms import FilterAnimalForm, FilterPeopleForm


class FiltersMixin(ContextMixin):
    """
    Бэк для блока панель фильтров
    """
    def get_context_data(self, **kwargs):
        context = super(FiltersMixin, self).get_context_data(**kwargs)
        context['filter_animal_form'] = FilterAnimalForm
        context['filter_people_form'] = FilterPeopleForm
        return context