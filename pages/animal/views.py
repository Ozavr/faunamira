from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

from pages.animal.models import Animal, AnimalAttr, KindAnimalAttr

from pages.animal.forms import AnimalForm, AnimalAttrForm


class AnimalView(TemplateView):
    """
    Страница профиля животного
    """
    template_name = 'animal.html'

    def get(self, request, *args, **kwargs):
        owner = get_object_or_404(Animal, id=kwargs.get('pk')).user
        if owner.is_active:
            return super(AnimalView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalView, self).get_context_data(**kwargs)
        context['animal'] = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        context['attrs'] = AnimalAttr.objects.filter(animal__pk=self.kwargs.get('pk'))
        context['people'] = get_object_or_404(Animal, pk=self.kwargs.get('pk')).user
        return context


class AnimalCreateView(CreateView):
    """
    Создание профиля животного
    """
    template_name = 'animal_create.html'
    model = Animal
    form_class = AnimalForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            return super(AnimalCreateView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def form_valid(self, form):
        an_obj = form.save(commit=False)
        an_obj.user = self.request.user
        return super(AnimalCreateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('animal', kwargs={'pk': self.object.id})


class AnimalUpdateView(UpdateView):
    """
    Редактирование животного
    """
    model = Animal
    template_name = 'animal_update.html'
    form_class = AnimalForm

    def get_animal(self):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return animal

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_animal()
        if (self.object.user == request.user) and self.object.user.is_active:
            self.form = AnimalForm(instance=self.object)
            return super(AnimalUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalUpdateView, self).get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        return context


class AnimalDeleteView(DeleteView):
    """
    Удаление животного
    """
    template_name = 'animal_delete.html'
    model = Animal

    def get(self, request, *args, **kwargs):
        self.obj = get_object_or_404(Animal, pk=self.kwargs["pk"])
        if (self.obj.user == request.user) and self.obj.user.is_active:
            return super(AnimalDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AnimalDeleteView, self).get_context_data(**kwargs)
        context['obj'] = self.obj
        return context

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'username': self.request.user})


class AttrCreateView(CreateView):
    """
    Добавления харатеристик животному
    """
    template_name = 'attr_create.html'
    model = AnimalAttr
    form_class = AnimalAttrForm

    def get_animal(self):
        animal = get_object_or_404(Animal, pk=self.kwargs.get('pk'))
        return animal

    def get_form(self):
        form = super(AttrCreateView, self).get_form()
        form.fields['attr'].queryset = KindAnimalAttr.objects.filter(kind=self.get_animal().kind)
        return form

    def get(self, request, *args, **kwargs):
        animal = self.get_animal()
        if (request.user == animal.user) and animal.user.is_active:
            return super(AttrCreateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def form_valid(self, form):
        animal = self.get_animal()
        obj = form.save(commit=False)
        obj.animal = animal
        obj.kind = animal.kind
        return super(AttrCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AttrCreateView, self).get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        return context


    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.kwargs.get('pk')})


class AttrUpdateView(UpdateView):
    """
    Редактирование атрибута
    """
    model = AnimalAttr
    template_name = 'attr_update.html'
    form_class = AnimalAttrForm

    def get_attr(self):
        return get_object_or_404(AnimalAttr, pk=self.kwargs.get('pk'))

    def get_form(self):
        form = super(AttrUpdateView, self).get_form()
        form.fields['attr'].queryset = KindAnimalAttr.objects.filter(kind=self.object.kind)
        return form

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.animal.pk})

    def get(self, request, *args, **kwargs):
        self.obj = self.get_attr()
        if (self.obj.animal.user == self.request.user) and self.obj.animal.user.is_active:
            self.form = AnimalAttrForm(instance=self.obj)
            return super(AttrUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AttrUpdateView, self).get_context_data(**kwargs)
        context['animal'] = get_object_or_404(Animal, pk=self.obj.animal.pk)
        return context


class AttrDeleteView(DeleteView):
    """
    Удаление атрибута
    """
    template_name = 'attr_delete.html'
    model = AnimalAttr

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(AnimalAttr, pk=self.kwargs["pk"])
        if (self.object.animal.user == request.user) and self.object.animal.user.is_active:
            return super(AttrDeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('home'))

    def get_context_data(self, **kwargs):
        context = super(AttrDeleteView, self).get_context_data(**kwargs)
        context['obj'] = self.object
        return context

    def get_success_url(self):
        return reverse_lazy('animal', kwargs={'pk': self.object.animal.pk})

