from django import forms
from django.utils.translation import ugettext_lazy as _

from pages.animal.models import Animal
from pages.userprofile.models import Profile


class FilterAnimalForm(forms.ModelForm):
    """
    Форма для фильтрации животных по определенным парметрам
    """
    age = forms.IntegerField(label=_('Age'), required=False,)
    class Meta:
        model = Animal
        fields = ['kind', 'gender', 'age']


class FilterPeopleForm(forms.ModelForm):
    """
    Форма для фильтрации пользователей по определенным параметрам
    """
    age = forms.IntegerField(label=_('Age'), required=False, )
    class Meta:
        model = Profile
        fields = ['gender', 'age', 'hobbies']