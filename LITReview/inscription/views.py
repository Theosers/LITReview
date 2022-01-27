from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from inscription.models import UserFollows, User

def logout_user(request):
    logout(request)
    return redirect(login_user)

def login_user(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect(flux)
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'inscription/accueil.html', context={'form': form, 'message': message})
def flux(request):
    return render(request, 'inscription/flux.html')

def inscription(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            p = Profil()
            # auto-login user
            login(request, user)
            return redirect(flux)

    return render(request, 'inscription/inscription.html', context={'form': form})

def abonnements(request):
    form = forms.FollowForm()
    message = ''
    follow = UserFollows.objects.all().filter(user=request.user)
    followed_by = UserFollows.objects.all().filter(followed_user=request.user)


    if request.method == 'POST':
        user_to_follow = request.POST.get('username')

        if User.objects.filter(username=user_to_follow).exists(): #remplace le if form.is_valid()
            user_to_follow_id = User.objects.get(username=user_to_follow)
            UserFollows.objects.get_or_create(user= request.user,followed_user= user_to_follow_id)

        else :
            message = 'Aucun utilisateur ne porte ce nom'


            #return redirect(abonnements)

    return render(request, 'inscription/abonnements.html', context={'form': form, 'follow': follow, 'followed_by' : followed_by, 'message' : message})