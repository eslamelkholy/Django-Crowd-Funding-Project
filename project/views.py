from django.db.models import Avg
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Add Project Form Validation
from .forms import ProjectForm
from .models import Project,Images,Report,Rating
from category.models import Category
from comments.models import Comments
from user.models import User
# List Specified Project
def listProject(request,id):
    user_project = Project.objects.filter(p_id = int(id)).first()
    comments = Comments.objects.filter(project_id = int(id))
    ratings= Rating.objects.filter(project_id=int(id))
    ratings_counter={rate.rate: len(ratings.filter(rate=rate.rate)) for rate in ratings}
    ratings_counter['count']=len(ratings)
    ratings_counter['avg']=ratings.aggregate(Avg('rate'))['rate__avg']
    if user_project:
        return render(request,"projects/projectPage.htm",
                {"project" : user_project,"comments" : comments, "ratings": ratings_counter})
    else:
        return HttpResponse("404 Not Found")


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
            new_project.current_amout = "0"
            new_project.user = User.objects.get(u_id = 1)
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


# Report Project Handler
def reportProject(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST['report_text']:
            newReport = Report()
            newReport.report_content = request.POST['report_text']
            newReport.user = User.objects.get(u_id = int(request.POST['user_id']))
            newReport.proejct = Project.objects.get(p_id = int(request.POST['project_id']))
            newReport.save()
            return JsonResponse({"done":"Done"})
        else:
            return JsonResponse({"error":"Error"})


# Project Home Page
def project(request):
    return render(request, "projects/projectHome.html")


# Project Donation
def donate_project(request,title):
    project_title = " ".join(title.split("-"))
    user_project = Project.objects.filter(title = project_title).first()
    if user_project:
        return render(request,"projects/donateProject.htm",{"project" : user_project})
    else:
        return HttpResponse("404 Not Found")


def rate_project(request):
    if request.method== 'POST':
        p_id=int(request['project_id'])
        u_id=int(request['user_id'])
        rate=int(request['rate'])
        print(p_id,u_id,rate)
        rate_record=Rating.objects.filter(project_id=p_id,user_id=u_id).update(rate=rate)
        if  rate_record:
            return JsonResponse({"done": "done"})
        else:
            try:
                Rating.objects.create(
                    project_id=Project.objects.get(p_id=p_id),
                    user_id=User.objects.get(u_id=u_id),
                    rate=rate
                )
            except:
                return JsonResponse({"error":"error"})
            else:
                return JsonResponse({"done": "done"})



