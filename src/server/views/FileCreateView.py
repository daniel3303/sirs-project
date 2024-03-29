import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate

from server.models import File

class FileCreateView(View):
    def get(self, request):
        return HttpResponse("Method not allowed. Use POST")

    def post(self, request):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)

        fileName = jsonRequestData.get("name", "")
        fileContent = jsonRequestData.get("content", "")
        username = jsonRequestData.get("username", "")
        password =jsonRequestData.get("password", "")

        # Check user authentication
        user = authenticate(username=username, password=password)
        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})


        file = File()
        file.setName(fileName)
        file.setContent(fileContent)
        file.setOwner(user)

        try:
            file.save()
        except Exception as ex:
            return JsonResponse({'status' : "error", "message" : "Ocorreu um erro ao criar o ficheiro. "+str(ex)})

        return JsonResponse({
                    'status' : "success",
                    'file' : {
                        'id' : file.getId(),
                        'name' : file.getName(),
                        'owner' : file.getOwner().getId(),
                        "corrupted" : file.isCorrupted(),
                        'permissions' : {
                            'read' : True,
                            'write' : True,
                        },
                    }
                })
