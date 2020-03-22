from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class Project(models.Model):
    p_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    details = models.CharField(max_length=200)
    total_target = models.IntegerField()
    current_amout = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    tags = models.CharField(max_length=200)
    category = models.ForeignKey("category.Category", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


# Image Class
class Images(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.ImageField(upload_to='images/')
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True)


# Donation Model
class Donation(models.Model):
    donate_id = models.AutoField(primary_key=True)
    donate_amount = models.IntegerField()
    project = models.ForeignKey("Project", on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


# Repor Project Model
class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_content = models.CharField(max_length=255)
    project = models.ForeignKey("Project",on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)


# Payment Class
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    amount = models.FloatField(null=True)
    timestamp  = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    project = models.ForeignKey("Project",on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.user.name


# Rating Model
class Rating(models.Model):
    class Meta:
         unique_together = (('project_id', 'user_id'),)

    project_id = models.ForeignKey("Project", on_delete=models.CASCADE, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    rate = models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=False)

    def __str__(self):
        return f"{self.user_id.fname} rates {self.project_id.title} with: {str(self.rate)}"
