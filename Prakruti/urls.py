"""Prakruti URL Configuration

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
from Prakruti_App import views

urlpatterns = [
    path("", views.index, name='landing'),
    path("signup/", views.signup and views.handleSignUp, name='signup'),
    path('login', views.handleLogin, name='handleLogin'),
    path('logout', views.handleLogout, name='handleLogout'),
    path("chPass", views.chPass, name='chPass'),
    path("home/", views.home, name='home'),
    
    # user
    path("analyze/", views.analyze, name='analysis'),
    path("recommend/", views.recommend, name='recommender'),
    path("shopping/", views.shopping, name='shopping'),
    path("profileU/", views.profileU, name='profileU'),

    # admin
    path("dashboard/", views.dashboard, name='dashboard'),
    path("patients/", views.patients, name='patients'),
    path("appointments/", views.appointments, name='appointments'),
    path("medicine_remedies/", views.M_remedies, name='M_remedies'),
    path("home_remedies/", views.H_remedies, name='H_remedies'),
    path("blogs/", views.blogs, name='blogs'),
    path("orders/", views.orders, name='orders'),
    path("A_profile/", views.A_profile, name='A_profile'),
    path("profileA/", views.profileA, name='profileA'),
    path("U_profile/", views.U_profile, name='U_profile'),
]
