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
stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

# List Specified Project 
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
            user_project = Project.objects.filter(p_id = request.POST['project_id']).first()
            return render(request,"projects/donateProject.htm",{"project" : user_project})

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            messages.error(request,f"{e.error.message}")
            return redirect("project")
        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.error(request,"Rate Limit Error")
            return redirect("project")
        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.error(request,"Invalid Request Error")
            return redirect("project")
        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.error(request,"Not Authentication")
            return redirect("project")
        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.error(request,"Network Error")
            return redirect("project")
        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.error(request,"Something Went Wrong.. You Were not Charged Please Try Again")
            return redirect("project")
        except Exception as e:
        # Send an email to ourselves
            messages.error(request,"A Serious Error Occured We Have been Notified")
            return redirect("project")
    else:
        return HttpResponse("404 Not Found")


def rate_project(request):
    if request.method== 'POST':
        p_id=int(request.POST['project_id'])
        u_id=int(request.POST['user_id'])
        rate=int(request.POST['rate'])
        rate_record=Rating.objects.filter(project_id_id=p_id,user_id_id=u_id).update(rate=rate)
        if rate_record:
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
                return JsonResponse({"RATE": "done"})
