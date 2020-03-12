from django.db import models
# Create your models here.
class Project(models.Model):
    p_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    details = models.CharField(max_length=200)
    total_target = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    project_images = models.ImageField(upload_to='images/')
    category = models.ForeignKey("category.Category",on_delete=models.CASCADE,null=True)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,null=True)