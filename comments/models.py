from django.db import models
# Create your models here.
class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_body = models.CharField(max_length=60)
    project = models.ForeignKey("project.Project",on_delete=models.CASCADE,null=True)
    user = models.ForeignKey("user.User",on_delete=models.CASCADE,null=True)