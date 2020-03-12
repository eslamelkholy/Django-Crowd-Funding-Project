from django import forms
from .models import *

class ProjectForm(forms.Form):
    title = forms.CharField(max_length=40,required=True)
    details = forms.CharField(max_length=200,required=True)
    total_target = forms.IntegerField(required=True)
    start_date = forms.DateField(required=True)
    end_date = forms.DateField(required=True)
    tags = forms.CharField(max_length=200)
    project_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
