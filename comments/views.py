from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core import serializers
# Add Project Form Validation
from .models import Comments
from user.models import User
from project.models import Project


def addComment(request):
    if request.is_ajax and request.method == 'POST':
        if request.POST['comment_content'] :
            newComment = Comments()
            newComment.comment_body = request.POST['comment_content']
            newComment.user = User.objects.get(u_id = int(request.POST['user_id']))
            newComment.project = Project.objects.get(p_id = int(request.POST['project_id']))
            newComment.save()
            ser_instance = serializers.serialize('json', [ newComment])
            return  JsonResponse({"data": ser_instance,"username":newComment.user.fname + ' ' + newComment.user.lname,"user_img": str(newComment.user.user_img)}, status=200)
        else:
            return JsonResponse({"error": "Please Fill The Comment"}, status=400)

