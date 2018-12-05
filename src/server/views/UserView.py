from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers

from server.models import User

class UserView(View):
    def get(self, request):
        users = []
        for user in User.objects.all().order_by('username'):
            users.append({
                    'id' : user.getId(),
                    'username' : user.getUsername(),
                    'name' : user.getName()
                    })
        return JsonResponse({ "status" : "success", "users": users})
