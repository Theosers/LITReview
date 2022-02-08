from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth import login, authenticate, logout
from inscription.models import UserFollows, User, Ticket, Review
from django.core.paginator import Paginator
from itertools import chain
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required

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


def inscription(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(flux)

    return render(request, 'inscription/inscription.html', context={'form': form})


@login_required
def abonnements(request):
    form = forms.FollowForm()
    message = ''
    follow = UserFollows.objects.all().filter(user=request.user)
    followed_by = UserFollows.objects.all().filter(followed_user=request.user)

    if request.method == 'POST':
        form = forms.FollowForm(request.POST)

        if request.POST.get('pk') != None:
            UserFollows.objects.filter(pk=request.POST['pk']).delete()
            return redirect(abonnements)

        elif request.POST.get('username') != None:
            user_to_follow = request.POST.get('username')
            if User.objects.filter(username=user_to_follow).exists():  # remplace le if form.is_valid()
                user_to_follow_id = User.objects.get(username=user_to_follow)
                UserFollows.objects.get_or_create(user=request.user, followed_user=user_to_follow_id)

            else:

                message = 'Aucun utilisateur ne porte ce nom'

    return render(request, 'inscription/abonnements.html',
                  context={'form': form, 'follow': follow, 'followed_by': followed_by, 'message': message})


@login_required
def create_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':

        form = forms.TicketForm(request.POST, request.FILES)

        if form.is_valid():
            ticket = Ticket(user=request.user, title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'], image=form.cleaned_data['image'])
            ticket.save()
            return redirect(flux)

    return render(request, 'inscription/create_ticket.html', context={'form': form})


@login_required
def flux(request):


    ticket_answer=''


    user_tickets = Ticket.objects.all().filter(user=request.user)
    user_reviews = Review.objects.all().filter(ticket__in=user_tickets).exclude(user=request.user)
    #les avis en réponse à ses propres tickets – même si l’utilisateur qui a répondu ne fait pas partie des personnes qu’il suit.
    follow = UserFollows.objects.all().filter(user=request.user)
    follower = [f.followed_user for f in follow] + [User.objects.filter(username=request.user)[0]]

    tickets = Ticket.objects.all().filter(user__in=follower)

    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all().filter(user__in=follower) | user_reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for item in page_obj.object_list:
        if item.content_type == 'TICKET' :
            ticket_answer = Review.objects.filter(ticket=item)


    return render(request, 'inscription/flux.html', context={'page_obj': page_obj, 'ticket_answer' : ticket_answer})


@login_required
def my_posts(request):
    tickets = Ticket.objects.all().filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    reviews = Review.objects.all().filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':

        if request.POST.get('pk_delete_ticket') != None:
            Ticket.objects.filter(pk=request.POST['pk_delete_ticket']).delete()
            return redirect(my_posts)
        elif request.POST.get('pk_modif_ticket') != None:
            request.session['ticket'] = request.POST.get('pk_modif_ticket')
            return redirect(modif_ticket)
        elif request.POST.get('pk_delete_review') != None:
            Review.objects.filter(pk=request.POST['pk_delete_review']).delete()
            return redirect(my_posts)
        elif request.POST.get('pk_modif_review') != None:
            request.session['review'] = request.POST.get('pk_modif_review')
            return redirect(modif_review)
    return render(request, 'inscription/my_posts.html', context={'page_obj': page_obj})


@login_required
def create_review(request):
    ticket_form = forms.TicketForm()
    review_form = forms.ReviewForm()

    if request.method == 'POST':

        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)

        if ticket_form.is_valid():
            ticket = Ticket(user=request.user, title=ticket_form.cleaned_data['title'],
                            description=ticket_form.cleaned_data['description'],
                            image=ticket_form.cleaned_data['image'])
            ticket.save()
        if review_form.is_valid():
            review = Review(ticket=ticket, headline=review_form.cleaned_data['headline'],
                            rating=review_form.cleaned_data['rating'], body=review_form.cleaned_data['body'],
                            user=request.user)
            review.save()

            return redirect(flux)

    return render(request, 'inscription/create_review.html',
                  context={'ticket_form': ticket_form, 'review_form': review_form})


def modif_ticket(request):
    ticket = Ticket.objects.get(id=request.session['ticket'])
    ticket_form = forms.TicketForm(instance=ticket)

    if request.method == 'POST':

        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():

            ticket.title = ticket_form.cleaned_data['title']
            ticket.description = ticket_form.cleaned_data['description']
            if ticket_form.cleaned_data['image'] == None:
                pass
            elif ticket_form.cleaned_data['image'] == False:
                ticket.image = None
            else:
                ticket.image = ticket_form.cleaned_data['image']
            ticket.save()
        return redirect(my_posts)

    return render(request, 'inscription/modif_ticket.html', context={'ticket_form': ticket_form})


def modif_review(request):
    review = Review.objects.get(id=request.session['review'])
    ticket_reviewed = review.ticket
    review_form = forms.ReviewForm(instance=review)

    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review.headline = review_form.cleaned_data['headline']
            review.body = review_form.cleaned_data['body']
            review.rating = review_form.cleaned_data['rating']
            review.save()
            return redirect(my_posts)

    return render(request, 'inscription/modif_review.html',
                  context={'review_form': review_form, 'ticket_reviewed': ticket_reviewed})


def create_review_answer(request):
    #ticket_reviewed = Ticket.objects.all()[0]

    review_form = forms.ReviewForm()
    if request.method == 'POST':
        print(request.POST.get('pk_mod_ticket'))
        ticket_reviewed = Ticket.objects.get(id=request.POST.get('pk_mod_ticket'))

        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = Review(headline=review_form.cleaned_data['headline'], body=review_form.cleaned_data['body'],
                            rating=review_form.cleaned_data['rating'], ticket=ticket_reviewed, user=request.user)
            review.save()
            return redirect(flux)

    return render(request, 'inscription/create_review_answer.html',
                  context={'ticket_reviewed': ticket_reviewed, 'review_form': review_form})
