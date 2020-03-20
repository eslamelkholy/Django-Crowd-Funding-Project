from django.shortcuts import render,redirect
from  django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpRequest
from django.contrib.auth import authenticate, login
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
    user=authenticate(request,username=request.POST['username'],password=request.POST['password'])
    # user.save()
    if user is not None:
        login(request,user)
        return redirect('/product')
    else:
        # message={"msg":"invalid password"}
        # return redirect('auth/login.html',message)
        # return redirect_to_login("product/", login_url=None)
        return HttpResponse(request.POST['username'])

def loginView(self):
    message={"msg":""}
    return render(self,'auth/login.html',message)
    
def registerView(self):
    return render(self,'auth/register.html')
 
def signup(request):
    username=request.POST["username"]    
    email=request.POST["email"]
    password=request.POST["password"]
    firstname=request.POST["firstname"]
    lastname=request.POST["lastname"]
    user=User.objects.create_user(username,email,password,firstname,lastname)
    user.save()
    # return redirect("/login_register/login")
    user=authenticate(username=request.POST['username'],password=request.POST['password'])
    return redirect("/project")

    # return HttpResponse(request.POST))


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
            user.set_unusable_password()
            user.save()

            

            # Send an email to the user with the token:
            # mail_subject = 'Activate your account.'
            # current_site = get_current_site(request)
            # uid = urlsafe_base64_encode(force_bytes(user.pk))
            # token = account_activation_token.make_token(user)
            # activation_link = "{0}/login_register/activate/?uidb64={1}/?token={2}".format(current_site, uid, token)
            # message = "Hello {0},\n {1}".format(user.username, activation_link)
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(mail_subject, message, to=[to_email])
            # email.send()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            # load a template like get_template() 
            # and calls its render() method immediately.
            message = render_to_string('auth/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
        else:
            return HttpResponse("fail")

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.user.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('product')
    else:
        return render(request, 'auth/account_activation_invalid.html')
def forgetPasswordView(self):
    return HttpResponse("forget password view")