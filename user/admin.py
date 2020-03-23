from django.contrib import admin
from project.models import Project,Donation,Images,Payment,Rating,Report
from category.models import Category
from user.models import Profile
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Images)
admin.site.register(Payment)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(Category)
admin.site.register(Profile)

# Register your models here.
