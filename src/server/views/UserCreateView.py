from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers

from server.models import User

class UserCreateView(View):
    def get(self, request):
        return HttpResponse("Method not allowed. Use POST")

    def post(self, request)
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST["name"]

        user = User()
