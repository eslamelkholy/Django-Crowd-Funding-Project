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

urlpatterns = [
    path('login/',auth_view.loginView,name="login"),
    path('signin/',auth_view.signin),
    # path('register/',auth_view.registerView,name="register"),
    path('register/', auth_view.Signup.as_view(), name='register'),
    path('signup/',auth_view.Signup.as_view()),
    path('forgetpassword/',auth_view.forgetPasswordView),
    # path('activate/<str:uid>/<str:token>', auth_view.activate, name='activate'),
    # url(r'^account_activation_sent/$', auth_view.account_activation_sent, name='account_activation_sent'),
    # url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_view.activate, name='activate'),


]
