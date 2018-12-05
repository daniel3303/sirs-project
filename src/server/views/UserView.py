from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.core import serializers

from server.models import User

class UserView(View):
    def get(self, request):
        return JsonResponse(serializers.serialize('json', User.objects.all()), safe=False)
