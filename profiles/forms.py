from django import forms
from django.contrib.auth.models import User
from user.models import Profile
from django.contrib.auth.forms import UserCreationForm


<<<<<<< HEAD

class UserForm(UserCreationForm):
    user_id=0
    def __init__(self, userId):
        super().__init__()
        UserForm.user_id=userId

    u_data = Profile.objects.filter(pk=user_id)
    for data in u_data:
        if data:
            first_name = forms.CharField(label="FirstName", widget=forms.TextInput(attrs={"value": data.user.first_name, "class":"form-control col-md-6"}))
            lname = forms.CharField(label="LastName", widget=forms.TextInput(attrs={"value": data.user.last_name, "class":"form-control col-md-6"}))
            email = forms.CharField(disabled=True,required=False, label="Email", widget=forms.EmailInput(attrs={"value": data.user.email, "class":"form-control col-md-6"}))
            password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"value": data.user.password, "class":"form-control col-md-6"}))
            phone = forms.CharField(label="Phone", widget=forms.NumberInput(attrs={"value": data.phone, "class":"form-control col-md-6"}))
            birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":'date',"class":"form-control col-md-6"}))
            fbprofile = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
            country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
            user_img = forms.ImageField(required=False,label="Profile Picture")

=======
class UserForm(forms.ModelForm):

    first_name = forms.CharField(required= False,label="FirstName", widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
    last_name = forms.CharField(required=False,label="LastName", widget=forms.TextInput(attrs={ "class":"form-control col-md-6"}))
    email = forms.CharField(disabled=True,required=False, label="Email", widget=forms.EmailInput(attrs={"class":"form-control col-md-6"}))
    password = forms.CharField(required=False,label="Password", widget=forms.PasswordInput(attrs={"class":"form-control col-md-6"}))
>>>>>>> 74537b96ccd5e68c03ce9629074e99964bcdc705

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
        ]


class ProfileForm(forms.ModelForm):

    phone = forms.CharField(required=False,label="Phone", widget=forms.NumberInput(attrs={"class":"form-control col-md-6"}))
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":'date',"class":"form-control col-md-6"}))
    fbprofile = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
    user_img = forms.ImageField(required=False,label="Profile Picture")

    class Meta:
        model = Profile
        fields = [
            'phone',
            'birthdate',
            'fbprofile',
            'country',
            'user_img',
            ]

