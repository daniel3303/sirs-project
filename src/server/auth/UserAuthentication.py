from server.models.User import User
from django.contrib.auth.hashers import *

class UserAuthentication:
    def authenticate(self, request, username=None, password=None):
        # Checks if it is a valid user
        print("Auth user: "+username+" password: "+password)

        try:
            user = User.objects.get(username=username)
            if(check_password(password, user.getPassword()) == True):
                print("auth success")
                return user
            else:
                print("auth failed")
                return None
        except User.DoesNotExist:
            print("auth failed")
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
