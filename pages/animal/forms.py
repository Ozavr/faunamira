from django.forms import ModelForm, inlineformset_factory, modelformset_factory


from pages.animal.models import Animal, AnimalAttr


class AnimalForm(ModelForm):

    class Meta:
        model = Animal
        fields = ['first_name', 'second_name', 'gender', 'info', 'birthday', 'kind', 'avatar']


class AnimalAttrForm(ModelForm):

    class Meta:
        model = AnimalAttr
        fields = ['attr', 'value']


#AnimalFormset = inlineformset_factory(Animal, AnimalAttr, fields=('attr', 'value'))
#AnimalFormset = modelformset_factory(AnimalAttr, form=AnimalAttrForm, fields=('attr', 'value'))