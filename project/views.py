from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Add Project Form Validation
# from .forms import ProjectForm 

#Add Project 
def addproject(request):
    return HttpResponse("Hello")
def project(request):
    return render(request, "projects/projectHome.html")