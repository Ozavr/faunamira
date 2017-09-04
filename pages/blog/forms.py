from django import forms
from tinymce.widgets import TinyMCE

from pages.blog.models import Blog


class BlogForm(forms.ModelForm):
    article = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Blog
        fields = ['title', 'article', 'date']