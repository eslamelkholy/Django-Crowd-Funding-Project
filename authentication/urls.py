"""crowd_funding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import authentication.views as auth_view
from django.conf.urls import url
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/',auth_view.loginView,name="login"),
    path('signin/',auth_view.signin),
    path('register/', auth_view.Signup.as_view(), name='register'),
    path('signup/',auth_view.Signup.as_view()),
    path('logout/',auth_view.logout_user),
    path('forgetpassword/',auth_views.PasswordResetView.as_view( template_name='auth/change-password.html',
            success_url = '/'),name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html'
         ),
         name='password_reset_done'),
    # url(r'^account_activation_sent/$', auth_view.account_activation_sent, name='account_activation_sent'),
   

]
