from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Note


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_admin']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
