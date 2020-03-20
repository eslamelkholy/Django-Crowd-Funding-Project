from django.conf import settings
from django.db.models import Avg
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
# Add Project Form Validation
from .forms import ProjectForm
from .models import Project,Images,Report,Payment
from category.models import Category
from comments.models import Comments
from user.models import User
# Stipe
import stripe
stripe.api_key = "sk_test_BfzJ6A79Q955Tt2DaVGrGKS900BMCGkffo"

# List Specified Project 
from .models import Project,Images,Report,Rating
from category.models import Category
from comments.models import Comments
from user.models import User
from django.views.decorators.csrf import csrf_exempt

# to get the similer projects baset on tags
def get_similer_projects(id):
    tags = [i for i in Project.objects.filter(p_id=id)[0].tags.split(" ")]
    similer_projects = [Project.objects.filter(tags__contains=i).exclude(p_id=id) for i in tags]
    similers = []
    for i in similer_projects:
        for j in i:
            try:
                project_image="image/"+str(j.images_set.first().image_name)
            except AttributeError:
                project_image=""
            j.image=project_image
            similers.append(j)
    similers = list(set(similers))[:4]
    return similers

# to get the rates and avg-rate of a project
def rate_projects(id):
    ratings= Rating.objects.filter(project_id=int(id))
    user_rating=ratings.get(user_id=1).rate
    ratings_counter={rate.rate: len(ratings.filter(rate=rate.rate)) for rate in ratings}
    ratings_counter['count']=len(ratings)
    ratings_counter['avg']=ratings.aggregate(Avg('rate'))['rate__avg']
    ratings_counter['thisRate']=user_rating
    return ratings_counter

# get project pictures
def get_project_images(id):
    project_images=list(Images.objects.filter(project=Project.objects.get(p_id=id)).values_list("image_name"))
    project_images=list(map(lambda tuple:tuple[0],project_images))
    project_images=map(lambda image_name:"image/"+image_name,project_images)
    return project_images

# List Specified Project
def listProject(request,id):
    user_project = Project.objects.filter(p_id = int(id)).first()
    comments = Comments.objects.filter(project_id = int(id))
    # rating projects
    ratings_counter=rate_projects(id)
    # similar projects
    similers=get_similer_projects(id)
    #project images
    project_images=get_project_images(id)
    if user_project:
        return render(request,"projects/projectPage.htm",
                {"project" : user_project,"comments" : comments,"images":project_images, "ratings": ratings_counter,"similars":similers})
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


# Project Donation Amout Page
def donate_project(request,title):
    project_title = " ".join(title.split("-"))
    if request.method == "GET" and Project.objects.filter(title = project_title).first():
        user_project = Project.objects.filter(title = project_title).first()
        return render(request,"projects/donateProject.htm",{"project" : user_project})
    else:
        return HttpResponse("404 Not Found Kid!!")

# Payment View
def payment_process(request):
    if request.method == 'POST':
        token = request.POST['stripeToken']
        amount = int(request.POST['amout_of_payment']) * 100
        user_project = Project.objects.filter(p_id = request.POST['project_id']).first()
        link = user_project.title.replace(" ","-")
        # Stipe Api Call & Error Handling
        try:
            charge = stripe.Charge.create(
                amount=amount, 
                currency="usd",
                source=token,
            )
            # Create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = User.objects.get(u_id = 1)
            payment.amout = amount
            payment.project = Project.objects.filter(p_id = request.POST['project_id']).first()
            payment.save()
            messages.success(request,"Your Donation Was Finished Successfully !")
            return render(request,"projects/donateProject.htm",{"project" : user_project})

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(request,f"{e.error.message}")
            return redirect(f"../project/{link}")
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.error(request,"Rate Limit Error")
            return redirect(f"../project/{link}")
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.error(request,"Invalid Request Error")
            return redirect(f"../project/{link}")
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.error(request,"Not Authentication")
            return redirect(f"../project/{link}")
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.error(request,"Network Error")
            return redirect(f"../project/{link}")
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.error(request,"Something Went Wrong.. You Were not Charged Please Try Again")
            return redirect(f"../project/{link}")
        except Exception as e:
        # Send an email to ourselves
            messages.error(request,"A Serious Error Occured We Have been Notified")
            return redirect(f"../project/{link}")
    else:
        return HttpResponse("404 Not Found")

def rate_project(request):
    if request.method== 'POST':
        p_id=int(request.POST['project_id'])
        u_id=int(request.POST['user_id'])
        rate=int(request.POST['rate'])
        rate_record=Rating.objects.filter(project_id_id=p_id,user_id_id=u_id).update(rate=rate)
        if rate_record:
            return JsonResponse({"done": rate})
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
                return JsonResponse({"done":rate})


def cancel_project(request):
    print("reached function!!!!")
    if request.method=="POST":
        u_id=request.POST['u_id']
        p_id=request.POST['p_id']
        this_project=Project.objects.get(p_id=p_id)
        if this_project:
            current_donation=this_project.current_amout
            total_target=this_project.total_target
            percentage=current_donation/total_target
            if percentage <0.25:
                # this_project.delete()
                return JsonResponse({"done":"done"})
            else:
                return JsonResponse({"not_approved":"not_approved"})
        else:
            return JsonResponse({"error"})




