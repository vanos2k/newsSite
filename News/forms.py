from django import forms
from .models import *
from django.core.exceptions import ValidationError


class BookForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['article_title', 'article_text']