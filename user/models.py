from django.db import models

# Create your models here.
class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    user_img = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.fname
    