"""crowdfunding URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from project import views as project_views
from comments import views as comment_views
import authentication.urls as auth
from django.conf.urls import url
import authentication.views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login_register/',include(auth)),
    path('profiles/', include('profiles.urls')),
    url('^api/v1/', include('social_django.urls', namespace='social')),
    path('activate/<slug:uid>/<slug:token>/', auth_view.activate, name='activate'),
    path('addproject',project_views.addproject),
    path('project/<int:id>',project_views.listProject),
    path('project',project_views.project),
    path('project/report',project_views.reportProject),
    path('project/addcomment',comment_views.addComment),
    path('project/report_comment',comment_views.reportComment),
    path('project/<str:title>', project_views.donate_project),
    path('payment/online',project_views.payment_process),
    path('rate/project',project_views.rate_project),
    path('cancel/project', project_views.cancel_project),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
