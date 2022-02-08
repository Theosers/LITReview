from django import forms
from inscription.models import Ticket, Review
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineRadios

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, widget=forms.TextInput(
        attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'}), label='')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput(
        attrs={'placeholder': 'Mot de passe', 'size': '40px', 'class': 'text-center'}), label='')


class SignupForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'}, ),
        label='')
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'size': '40px', 'class': 'text-center'}, ),
        label='')
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirmer mot de passe', 'size': '40px', 'class': 'text-center'}, ), label='')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')


class FollowForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'size': '40px', 'class': 'text-center'}, ),
        label='')


class TicketForm(forms.ModelForm):
    # title = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size' : '100px'}))
    # description = forms.CharField(max_length=2048, widget=forms.Textarea(attrs={'cols': '100'}))
    # image = forms.ImageField(required=False)

    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    # headline = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size' : '100px'}))
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class' : 'form-check form-check-inline'}), choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    # body = forms.CharField(max_length=8192, widget=forms.Textarea(attrs={'cols': '100'}))

    class Meta:
        model = Review
        fields = ("headline", "rating", "body")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
                InlineRadios('rating')
        )