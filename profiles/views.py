from django.shortcuts import render, get_object_or_404
from project.models import Project, Donation
from user.models import User


# Create your views here.
def index(request):
    u_data = User.objects.filter(u_id=2)
    context = {
        'u_data': u_data
    }
    return render(request, 'profiles/index.html', context)


def projects(request):
    u_data = User.objects.filter(pk=2)
    p_data = Project.objects.filter(user_id=2)
    context = {
        'u_data': u_data,
        'p_data': p_data
    }
    return render(request, 'profiles/projects.html', context)


def donations(request):
    u_data = User.objects.filter(pk=2)
    p_data = Project.objects.filter(user_id=2)
    d_data = Donation.objects.filter(user_id=2)
    context = {
        'u_data': u_data,
        'p_data': p_data,
        'd_data' : d_data,
    }
    return render(request, 'profiles/donations.html', context)


def edit(request):
    context ={}
    return render(request, 'profiles/edit.html', context)