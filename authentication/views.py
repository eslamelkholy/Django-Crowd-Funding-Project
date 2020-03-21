from django.shortcuts import render,redirect
from  django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpRequest
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import redirect_to_login
from django.views import View
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
# Create your views here.
def signin(request):
    #check if user exist
    user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
    if user is not None:
        login(request,user)
        return redirect("/project")
    else:
        return HttpResponse(user)

def loginView(self):
    message={"msg":""}
    return render(self,'auth/login.html',message)
    
def registerView(self):
    return render(self,'auth/register.html')

def logout_user(request):
    logout(request)
    return redirect("/product")

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'auth/register.html',{"form":form})

    def post(self, request):
        user1={}
        user1["username"]=request.POST["username"]        
        user1["first_name"]=request.POST["first_name"]
        user1["last_name"]=request.POST["last_name"]
        user1["email"]=request.POST["email"]
        user1["password1"]=request.POST["password1"]
        user1["password2"]=request.POST["password2"]
        form = SignupForm(user1)
        if form.is_valid():
            # Create an inactive user with no password:
            user = form.save(commit=False)
                
            user.is_active = False
            user.set_password(request.POST["password1"])
            user.save()

            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            try:
                message = render_to_string('auth/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
            except AttributeError:
                message = render_to_string('auth/activation_request.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': user.pk ,
                    # method will generate a hash value with user related data
                    'token': account_activation_token.make_token(user),
                })
            user.email_user(subject, message)
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        else:
            return HttpResponse("errors in validations")

def activate(request, uidb64, token,backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except ValueError:
        uid=uidb64
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user,backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'auth/success.html')
    else:
        return HttpResponse("activation failed")
def forgetPasswordView(self):
    return HttpResponse("forget password view")