from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers
from django.contrib.auth import authenticate

from server.models import File

# Returns a list of files for a given user
class FileListView(View):
    def get(self, request):
        username = request.GET.get("username", "")
        password = request.GET.get("password", "")
        user = authenticate(username=username, password=password)

        if(user is None):
            return JsonResponse({ "status" : "error", "message": "Autenticação falhou. Utilizador ou password errados."})


        files = []
        for file in user.files.all():
            files.append({
                    'id' : file.getId(),
                    'name' : file.getName()
                    })
        return JsonResponse({ "status" : "success", "files": files})
