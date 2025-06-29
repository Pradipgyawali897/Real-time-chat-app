# r_chat/forms.py
from django import forms
from .models import ChatGroup, GroupMessage
from django.contrib.auth.models import User

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
    friends = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'text-gray-400',
        }),
        required=False,
        label="Add Friends to Group"
    )

    class Meta:
        model = ChatGroup
        fields = ['group_name', 'picture', 'friends']
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

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['friends'].queryset = User.objects.filter(
                id__in=user.friendships_sent.values_list('to_user', flat=True)
            )

    def clean_group_name(self):
        group_name = self.cleaned_data['group_name']
        if len(group_name) < 3:
            raise forms.ValidationError("Group name must be at least 3 characters long.")
        return group_name