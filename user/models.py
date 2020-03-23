from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class User(models.Model):

    # user=models.OneToOneField(User,on_delete=models.CASCADE)
    # u_id = models.AutoField(primary_key=True)
    # fname = models.CharField(max_length=50)
    # lname = models.CharField(max_length=50)
    # email = models.EmailField(max_length=200)
    # password = models.CharField(max_length=50)
    # phone = models.CharField(default="",max_length=30)
    # user_img = models.ImageField(default="",upload_to='images/')
    # email_confirmed = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.fname
    # Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,null=False,on_delete=models.CASCADE)
    # user=models.ForeignKey(User, on_delete=models.CASCADE, null=False,unique=True)
    # u_id = models.AutoField(primary_key=True)
    # fname = models.CharField(max_length=50)
    # lname = models.CharField(max_length=50)
    # email = models.EmailField(max_length=200)
    # password = models.CharField(max_length=50)
    phone = models.CharField(default="",max_length=30)
    user_img = models.ImageField(default="",upload_to='images/')
    # email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
