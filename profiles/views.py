from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from project.models import Project, Donation
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth import authenticate

# from .forms import UserForm


# Create your views here.
def index(request):
    u_data = Profile.objects.filter(user_id=request.session['id'])
    context = {
        'u_data': u_data
    }
    return render(request, 'profiles/index.html', context)


def projects(request):
    u_data = Profile.objects.filter(user_id=request.session['id'])
    p_data = Project.objects.filter(user_id=request.session['id'])
    context = {
        'u_data': u_data,
        'p_data': p_data
    }
    return render(request, 'profiles/projects.html', context)

@login_required()
def donations(request):
    u_data = Profile.objects.filter(user_id=request.session['id'])
    p_data = Project.objects.filter(user_id=request.session['id'])
    d_data = Donation.objects.filter(user_id=request.session['id'])
    context = {
        'u_data': u_data,
        'p_data': p_data,
        'd_data': d_data,
    }
    return render(request, 'profiles/donations.html', context)

@login_required()
def edit(request):
    print("request",request)
    u_data = Profile.objects.filter(user_id=request.session['id'])
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            for data in u_data:
                myid = request.session['id']
                data.user.first_name = request.POST.get('fname',False)
                data.user.last_name = request.POST.get('lname',False)
                data.user.password = request.POST.get('password',False)
                data.phone = request.POST.get('phone',False)
                data.birthdate = request.POST.get('birthdate',False)
                data.fbprofile = request.POST.get('fbprofile',False)
                data.country = request.POST.get('country',False)
                user_img = request.FILES.getlist('user_img')[0]
                fs = FileSystemStorage()
                filename = fs.save(user_img.name, user_img)
                data.user_img=filename
                data.save()
        else:
            print("erorr")

    else:
        form = UserForm()

    p_data = Project.objects.filter(user_id=request.session['id'])
    d_data = Donation.objects.filter(user_id=request.session['id'])

    context = {
        'u_data': u_data,
        'p_data': p_data,
        'd_data': d_data,
        'form': form,
    }
    return render(request, 'profiles/edit.html', context)


def delete(request):
    u_data = Profile.objects.filter(user_id=request.session['id'])
    p_data = Project.objects.filter(user_id=request.session['id'])
    d_data = Donation.objects.filter(user_id=request.session['id'])

    if request.method == 'GET' and 'password' in request.GET:
        out = authenticate(request, username=request.GET['name'], password=request.GET['password'])
        if out is not None:
            try:
                Profile.objects.get(user_id=request.session['id']).delete()
                User.objects.get(pk=request.session['id']).delete()

            except:
                return JsonResponse({"deleted":False})
            else:
                return JsonResponse({"deleted":True})
        else:
            raise PermissionDenied
    else:
        context = {
            'u_data': u_data,
            'p_data': p_data,
            'd_data': d_data,
        }

    return render(request, 'profiles/delete_user.html', context)

