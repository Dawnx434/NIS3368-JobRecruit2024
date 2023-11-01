from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):

    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': '输入标题'}
        ),
        label='标题',
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': '输入内容'}
        ),
        max_length=4000,
        label='内容',
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['message', ]
