from django.forms import ModelForm
from django import forms
from .models import *

class CreateMessage(ModelForm):
    class Meta:
        model = GroupMessages
        fields = ['body']
        widgets = {
             'body' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength' : '300', 'autofocus': True }),
        }


class CreateGroup(ModelForm):
    class Meta:
        model=ChatGroup
        fields=['group_name','picture']

