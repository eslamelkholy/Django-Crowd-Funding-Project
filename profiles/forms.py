from django import forms
from django.contrib.auth.models import User
from user.models import Profile


class UserForm(forms.ModelForm):

    u_data = Profile.objects.filter(pk=3)
    for data in u_data:
        if data:
            first_name = forms.CharField(label="FirstName", widget=forms.TextInput(attrs={"value": data.user.first_name, "class":"form-control col-md-6"}))
            last_name = forms.CharField(label="LastName", widget=forms.TextInput(attrs={"value": data.user.last_name, "class":"form-control col-md-6"}))
            email = forms.CharField(disabled=True,required=False, label="Email", widget=forms.EmailInput(attrs={"value": data.user.email, "class":"form-control col-md-6"}))
            password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"value": data.user.password, "class":"form-control col-md-6"}))
            phone = forms.CharField(label="Phone", widget=forms.NumberInput(attrs={"value": data.phone, "class":"form-control col-md-6"}))
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


"""
    'user[first_name]',
            'user.last_name',
            'user.email',
            'user.password',
"""