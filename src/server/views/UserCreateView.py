import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers

from server.models import User

class UserCreateView(View):
    def get(self, request):
        return HttpResponse("Method not allowed. Use POST")

    def post(self, request):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)


        username = jsonRequestData["username"]
        password =jsonRequestData["password"]
        name = jsonRequestData["name"]

        user = User()
        user.setUsername(username)
        user.setPassword(password)
        user.setName(name)


        try:
            # Save may raise an exception (for example if the username is already in use)
            user.save()
        except Exception as ex:
            return JsonResponse({'status' : "error", "message" : "O username escolhido já existe."})

        return JsonResponse({
                'status' : "success",
                "message": "Registo efetuado com sucesso.",
                "username" : user.getUsername(),
                "name": user.getName(),
                "userId" : user.getId()
        })
