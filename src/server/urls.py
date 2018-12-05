from django.urls import path

from server.views import UserView
from server.views import UserCreateView

urlpatterns = [
    path('users', UserView.as_view()),
    path('users/create', UserCreateView.as_view()),
]
