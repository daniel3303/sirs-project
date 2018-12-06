import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate

from server.models import File
from server.models import User
from server.models import Role

class FileRolesView(View):
    def get(self, request, id=0):
        # Check user authentication
        username = request.GET.get("username", "")
        password = request.GET.get("password", "")
        user = authenticate(username=username, password=password)

        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})

        # Load the file
        try:
            file = user.files.get(id=id)

            roles = []
            for role in file.editors.all():
                roles.append({
                    'write' : role.canWrite(),
                    'read' : role.canRead(),
                    'user' : {
                        'id' : role.getUser().getId(),
                        'username' : role.getUser().getUsername(),
                        'name' : role.getUser().getName(),
                    }
                })


            return JsonResponse({
                "status" : "success",
                "roles" : roles,
                })

        except File.DoesNotExist:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })


    def post(self, request, id=0):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)

        targetUserId = jsonRequestData.get("userId", 0)
        canRead = jsonRequestData.get("read", False)
        canWrite = jsonRequestData.get("write", False)

        username = jsonRequestData["username"]
        password =jsonRequestData["password"]

        # Check user authentication
        user = authenticate(username=username, password=password)
        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})


        # Load the file
        file = None
        try:
            file = user.files.get(id=id)
        except File.DoesNotExist as ex:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })


        # Load the target user
        targetUser = None
        try:
            targetUser = User.objects.get(id=targetUserId)
        except User.DoesNotExist as ex:
            return JsonResponse({
                "status" : "error",
                "message" : "O utilizador a quem pretende adicionar permissões não foi encontrado."
            })

            #role = Role()
            #role.setUser(targetUser)
            #role.setReadPermission(canRead)
            #role.setWritePermission(canWrite)
            #role.setFile(file)
            #role.save()


        return JsonResponse({'status' : "success"})
