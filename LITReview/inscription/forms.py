from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'}), label='')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'size': '40px', 'class': 'text-center'}), label='')



class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'},),label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'size': '40px', 'class': 'text-center'}, ),label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirmer mot de passe', 'size': '40px', 'class': 'text-center'}, ), label='')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username','password1', 'password2')


class FollowForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'}, ),
        label='')