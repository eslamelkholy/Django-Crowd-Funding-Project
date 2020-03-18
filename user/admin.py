from django.contrib import admin
from project.models import Project,Donation,Images,Payment,Rating,Report
from user.models import User
from category.models import Category

admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Images)
admin.site.register(Payment)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(User)
admin.site.register(Category)

# Register your models here.
