from django.core.exceptions import PermissionDenied
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core import serializers
# Add Project Form Validation
from .models import Comments,ReportComment
from project.models import Project
from django.contrib.auth.models import User
from user.models import Profile

# Add Comment
def addComment(request):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == 'POST':
            if request.POST['comment_content'] :
                newComment = Comments()
                newComment.comment_body = request.POST['comment_content']
                newComment.profile = Profile.objects.get(user_id = int(request.session['id']))
                newComment.project = Project.objects.get(p_id = int(request.POST['project_id']))
                newComment.save()
                ser_instance = serializers.serialize('json', [ newComment])
                return  JsonResponse({"data": ser_instance,"username":newComment.profile.user.first_name + ' ' + newComment.profile.user.last_name,"c_id" : newComment.comment_id,"user_img": str(newComment.profile.user_img)}, status=200)
            else:
                return JsonResponse({"error": "Please Fill The Comment"}, status=400)
    else:
        raise PermissionDenied


# Report Specified Comment
def reportComment(request):
    if request.user.is_authenticated:
        if request.is_ajax and request.method == 'POST':
            if request.POST['report_content']:
                new_report = ReportComment()
                new_report.report_content = request.POST['report_content']
                new_report.comment = Comments.objects.get(comment_id = int(request.POST['comment_id']))
                new_report.profile = Profile.objects.get(user_id = int(request.session['id']))
                new_report.save()
                return JsonResponse({"id" : "Done"})
            else:
                return JsonResponse({"error" : "Error"})
    else:
        raise PermissionDenied
