from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme sua senha', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'handle', 'email', 'bio', 'profile_pic', 'location', 'birth_date', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Seu nome de usuário (@)")
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
