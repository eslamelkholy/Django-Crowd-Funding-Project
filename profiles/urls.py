from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.projects, name='projects'),
    path('donations/', views.donations, name='donations'),
    path('edit/', views.edit, name='edit'),
]
