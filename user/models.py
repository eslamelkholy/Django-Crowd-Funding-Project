from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,null=False,on_delete=models.CASCADE)

    phone = models.CharField(default="",max_length=30)
    user_img = models.ImageField(default="",upload_to='images/')
    fbprofile = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=50, null=True)
    birthdate = models.DateField(null=True)

    # email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user
