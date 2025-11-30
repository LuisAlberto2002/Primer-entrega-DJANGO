from django import forms
from django.contrib.auth.models import User
from .models import Comments
from django.contrib.auth.forms import AuthenticationForm


class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CommentForm(forms.ModelForm):
    comment = forms.CharField()
    class Meta:
        model = Comments
        fields = ['comment']        
