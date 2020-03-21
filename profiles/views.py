from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from project.models import Project, Donation
from user.models import User
from .forms import UserForm


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
        'd_data': d_data,
    }
    return render(request, 'profiles/donations.html', context)


def edit(request):
    print("request",request)
    u_data = User.objects.filter(pk=2)
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            for user in u_data:
                user.fname = request.POST['fname']
                user.lname = request.POST['lname']
                user.password = request.POST['password']
                user.phone = request.POST['phone']
                user.birthdate = request.POST['birthdate']
                user.fbprofile = request.POST['fbprofile']
                user.country = request.POST['country']
                user_img = request.FILES.getlist('user_img')[0]
                fs = FileSystemStorage()
                filename = fs.save(user_img.name, user_img)
                user.user_img=filename
                user.save()
        else:
            print("erorr")

    else:
        form = UserForm()

    p_data = Project.objects.filter(user_id=2)
    d_data = Donation.objects.filter(user_id=2)

    context = {
        'u_data': u_data,
        'p_data': p_data,
        'd_data': d_data,
        'form': form,
    }
    return render(request, 'profiles/edit.html', context)


def delete(request):

    u_data = User.objects.filter(pk=3)
    p_data = Project.objects.filter(user_id=3)
    d_data = Donation.objects.filter(user_id=3)
    if request.method == 'GET' and 'id' in request.GET:
        try:
            User.objects.get(pk=3).delete()
        except:
            return JsonResponse({"deleted":False})
        else:
            return JsonResponse({"deleted":True})
    else:
        context = {
            'u_data': u_data,
            'p_data': p_data,
            'd_data': d_data,
        }

    return render(request, 'profiles/delete_user.html', context)

