from django import forms
from .models import Message
from django.contrib.auth.models import User

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=User.objects.all(), label='Recipient')

    class Meta:
        model = Message
        fields = ['recipient', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}),
        }