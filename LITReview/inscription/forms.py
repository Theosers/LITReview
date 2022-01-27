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

class TicketForm(forms.Form):
    title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size' : '100px'}))
    description = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'cols': '100'}))
    image = forms.ImageField()
