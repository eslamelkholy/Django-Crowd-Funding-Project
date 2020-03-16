from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpRequest
from django.contrib.auth import authenticate, login

# Create your views here.
def signin(request):
    user=authenticate(username=request.POST['username'],password=request.POST['password'])
    # user.save()
    if user is not None:
        login(request,user)
        return redirect('/home')
    else:
        return render(request,'auth/fail.html')
def loginView(self):
    return render(self,'auth/login.html')
    
