from django import forms

from pages.messager.models import Dialog, Message


class DialogForm(forms.ModelForm):
    """
    Форма для создания диалога
    """
    class Meta:
        model = Dialog
        fields = ['user_to',]


class MessageForm(forms.ModelForm):
    """
    Форма для создания сообщения
    """
    class Meta:
        model = Message
        fields = ['message',]