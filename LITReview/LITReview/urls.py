"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inscription import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accueil/', views.login_user, name='accueil'),
    path('logout/', views.logout_user, name='logout'),
    path('flux/', views.flux, name='flux'),
    path('accueil/inscription/', views.inscription),
    path('abonnements/', views.abonnements, name='abonnements'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('my_posts', views.my_posts, name='my_posts'),
    path('create_review/', views.create_review, name='create_review'),
    path('modif_ticket/', views.modif_ticket, name='modif_ticket'),
    path('modif_review/', views.modif_review, name='modif_review'),
    path('create_review_answer/', views.create_review_answer, name='create_review_answer')
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
