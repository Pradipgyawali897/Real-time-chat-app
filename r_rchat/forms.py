# r_rchat/forms.py
from django import forms
from .models import ChatGroup, GroupMessage

class CreateMessage(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': 'Add message ...',
                'class': 'p-4 text-black',
                'maxlength': '300',
                'autofocus': True
            }),
        }

class CreateGroup(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['group_name', 'picture']
        widgets = {
            'group_name': forms.TextInput(attrs={
                'class': 'w-full bg-gray-800 text-white p-2 rounded-lg mb-2',
                'placeholder': 'Enter group name',
                'required': 'required',
            }),
            'picture': forms.FileInput(attrs={
                'class': 'w-full text-gray-400 p-2 rounded-lg',
            }),
        }

    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        if len(group_name) < 3:
            raise forms.ValidationError("Group name must be at least 3 characters long.")
        return group_name