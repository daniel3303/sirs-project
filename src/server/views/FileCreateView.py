import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers

from server.models import File

class FileCreateView(View):
    def get(self, request):
        return HttpResponse("Method not allowed. Use POST")

    def post(self, request):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)


        fileName = jsonRequestData["name"]
        username = jsonRequestData["username"]
        password =jsonRequestData["password"]

        # Check user authentication
        user = authenticate(username=username, password=password)
        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})


        file = File()
        file.setName(fileName)
        file.setOwner(user)

        try:
            file.save()
        except:
            return JsonResponse({'status' : "error", "message" : "Ocorreu um erro ao criar o ficheiro."})

        return JsonResponse({'status' : "success"})
