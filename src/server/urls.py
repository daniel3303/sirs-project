from django.urls import path

from server.views import UserView
from server.views import UserCreateView

from server.views import FileListView
from server.views import FileCreateView
from server.views import FileView

urlpatterns = [
    path('users', UserView.as_view()),
    path('users/create', UserCreateView.as_view()),

    path('files', FileListView.as_view()),
    path('files/create', FileCreateView.as_view()),
    path('files/<int:id>/', FileView.as_view()),
]
