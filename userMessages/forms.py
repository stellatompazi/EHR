from django import forms
from userMessages.models import *


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('sender', 'content')
        widgets = {
            'sender': forms.HiddenInput(),
            #'receiver': forms.HiddenInput(),
            #'created_at': forms.DateInput(attrs={'type': 'datetime-local'}, format= '%d-%m-%Y T%H:%M')
        }