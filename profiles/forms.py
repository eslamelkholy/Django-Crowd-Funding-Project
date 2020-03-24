from django import forms
from django.contrib.auth.models import User
from user.models import Profile


class UserForm(forms.ModelForm):

    first_name = forms.CharField(required= False,label="FirstName", widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
    last_name = forms.CharField(required=False,label="LastName", widget=forms.TextInput(attrs={ "class":"form-control col-md-6"}))
    email = forms.CharField(disabled=True,required=False, label="Email", widget=forms.EmailInput(attrs={"class":"form-control col-md-6"}))
    password = forms.CharField(required=False,label="Password", widget=forms.PasswordInput(attrs={"class":"form-control col-md-6"}))

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

