from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Add Project Form Validation
from .forms import ProjectForm
from .models import Project,Images
from category.models import Category

# List Specified Project 
def listProject(request,id):
    return render(request,"projects/projectPage.htm")


# Add Project
def addproject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)

        if form.is_valid():
            
            new_project = Project()
            new_project.title = request.POST['title']
            new_project.details = request.POST['details']
            new_project.total_target = request.POST['total_target']
            new_project.start_date = request.POST['start_date']
            new_project.end_date = request.POST['end_date']
            new_project.tags = request.POST['tags']
            new_project.category = Category.objects.get(cat_id = int(request.POST['category']))
            new_project.save()
            # MultiPle Image Section
            images = request.FILES.getlist('project_images')
            for image in images:
                fs = FileSystemStorage()
                filename = fs.save(image.name,image)
                new_image = Images()
                new_image.image_name = filename
                new_image.project = new_project
                new_image.save()
            messages.success(request,'Project Has Been Created Successfully')
        else:
            messages.error(request,"Please Fill Required Fields")
        categories = Category.objects.all()
        return render(request,"projects/addproject.htm",{"form":form,"categories" : categories})
    else:
        categories = Category.objects.all()
        context = {"categories" : categories}
        return render(request, "projects/addproject.htm",context)


#Project Home Page
def project(request):
    return render(request, "projects/projectHome.html")