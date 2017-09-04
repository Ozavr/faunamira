from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404

from pages.messager.forms import DialogForm, MessageForm
from pages.messager.models import Dialog, Message


class DialogsView(CreateView):
    """
    Стриница с просмотром и созданием диалога
    """
    model = Dialog
    template_name = 'dialogs.html'
    form_class = DialogForm

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return super(DialogsView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(DialogsView, self).get_context_data(**kwargs)
        context['dialogs'] = Dialog.objects.filter(Q(user_from=self.request.user) | Q(user_to=self.request.user))
        return context

    def form_valid(self, form):
        self.dialog = form.save(commit=False)
        self.dialog.user_from = self.request.user
        return super(DialogsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('message', kwargs={'pk': self.dialog.pk})


class MessagesView(CreateView):
    """
    Страница с сообщениями определенного диалога
    """
    model = Dialog
    template_name = 'chat.html'
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return super(MessagesView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        context['dialog'] = get_object_or_404(Dialog, pk=self.kwargs.get('pk'))
        context['messages'] = Message.objects.filter(dialog__pk=self.kwargs.get('pk')).order_by('date')
        return context

    def form_valid(self, form):
        message = form.save(commit=False)
        message.dialog = get_object_or_404(Dialog, pk=self.kwargs.get('pk'))
        message.user_from = self.request.user
        return super(MessagesView, self).form_valid(form)

    def get_success_url(self):
        return reverse('message', kwargs={'pk': self.kwargs.get('pk')})