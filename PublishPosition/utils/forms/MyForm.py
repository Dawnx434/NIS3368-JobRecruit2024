from django import forms
from mdeditor.fields import MDTextFormField


class PublishPositionForm(forms.Form):
    content = MDTextFormField(label="")
