import json

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate

from server.models import File

class FileView(View):
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
            return JsonResponse({
                "status" : "success",
                "file" : {
                    "id" : file.getId(),
                    "name" : file.getName(),
                    "content" : file.getContent()
                }
            })
        except File.DoesNotExist:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })

    def post(self, request, id=0):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)

        # Check user authentication
        username = jsonRequestData["username"]
        password = jsonRequestData["password"]

        user = authenticate(username=username, password=password)
        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})


        # Load the file
        try:
            file = user.files.get(id=id)

            content = jsonRequestData.get("content", None)
            if content is not None:
                file.setContent(content)

            name = jsonRequestData.get("name", None)
            if name is not None:
                file.setName(name)

            try:
                file.save()
            except Exception as ex:
                return JsonResponse({'status' : "error", "message" : "Ocorreu um erro ao atualizar o ficheiro. " +str(ex)})

            return JsonResponse({'status' : "success"})
        except File.DoesNotExist:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })

        except File.DoesNotExist:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })

    # Delete the file with a given id
    def delete(self, request, id = 0):
        bodyUnicode = request.body.decode('utf-8')
        jsonRequestData = json.loads(bodyUnicode)

        # Check user authentication
        username = jsonRequestData["username"]
        password = jsonRequestData["password"]

        user = authenticate(username=username, password=password)
        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})

        # Load the file
        try:
            file = user.files.get(id=id)
            file.delete()
            return JsonResponse({'status' : "success"})

        except File.DoesNotExist:
            return JsonResponse({
                "status" : "error",
                "message" : "Ficheiro não encontrado."
            })
