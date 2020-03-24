from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from project.models import Project, Donation
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserForm,ProfileForm
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
        u_form = UserForm(request.POST,request.FILES)
        p_form = ProfileForm(request.POST,request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            for data in u_data:
                data.user.first_name = request.POST['first_name']
                data.user.last_name = request.POST['last_name']
                data.user.password = request.POST['password']
                data.phone = request.POST['phone']
                data.birthdate = request.POST['birthdate']
                data.fbprofile = request.POST['fbprofile']
                data.country = request.POST['country']
                user_img = request.FILES.getlist('user_img')[0]
                fs = FileSystemStorage()
                filename = fs.save(user_img.name, user_img)
                data.user_img=filename
                data.save()
        else:
            print("erorr")

    else:
        obj1 = User.objects.get(pk=request.session['id'])
        obj2 = Profile.objects.get(user_id=request.session['id'])
        u_form = UserForm(instance=obj1)
        p_form = ProfileForm(instance=obj2)

    p_data = Project.objects.filter(user_id=request.session['id'])
    d_data = Donation.objects.filter(user_id=request.session['id'])

    context = {
        'u_data': u_data,
        'p_data': p_data,
        'd_data': d_data,
        'u_form': u_form,
        'p_form':p_form,
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

