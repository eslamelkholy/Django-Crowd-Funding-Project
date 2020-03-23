# from django import forms
# from user.models import User
#
#
# class UserForm(forms.ModelForm):
#
#     u_data = User.objects.filter(pk=2)
#     for user in u_data:
#         if user:
#             fname = forms.CharField(label="FirstName", widget=forms.TextInput(attrs={"value": user.fname, "class":"form-control col-md-6"}))
#             lname = forms.CharField(label="LastName", widget=forms.TextInput(attrs={"value": user.lname, "class":"form-control col-md-6"}))
#             email = forms.CharField(disabled=True,required=False, label="Email", widget=forms.EmailInput(attrs={"value": user.email, "class":"form-control col-md-6"}))
#             password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"value": user.password, "class":"form-control col-md-6"}))
#             phone = forms.CharField(label="Phone", widget=forms.NumberInput(attrs={"value": user.phone, "class":"form-control col-md-6"}))
#             birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={"type":'date',"class":"form-control col-md-6"}))
#             fbprofile = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
#             country = forms.CharField(required=False, widget=forms.TextInput(attrs={"class":"form-control col-md-6"}))
#             user_img = forms.ImageField(required=False,label="Profile Picture")
#
#     class Meta:
#         model = User
#         fields = [
#             'fname',
#             'lname',
#             'email',
#             'password',
#             'phone',
#             'birthdate',
#             'fbprofile',
#             'country',
#             'user_img',
#         ]