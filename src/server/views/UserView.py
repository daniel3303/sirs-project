from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate
import json

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

    # Check user credentials
    def post(self, request):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)

        # Check user authentication
        username = jsonRequestData["username"]
        password = jsonRequestData["password"]

        user = authenticate(username=username, password=password)

        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou."})
        else:
            return JsonResponse({
                        "status" : "success",
                        "message": "Autenticação efectuada com sucesso.",
                        "username" : user.getUsername(),
                        "name": user.getName(),
                        "userId" : user.getId()
            })
