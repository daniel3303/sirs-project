from server.models.User import User
from django.contrib.auth.hashers import *

class UserAuthentication:
    def authenticate(self, request, username=None, password=None):
        # Checks if it is a valid user
        try:
            user = User.objects.get(username=username)
            if(check_password(password, user.getPassword()) == True):
                if(user.isCorrupted() == True):
                    print("Authentication blocked for '"+username+"'. User corrupted.")
                    return None
                else:
                    print("Authentication successed for '"+username+"'.")
                    return user
            else:
                print("Authentication failed for '"+username+"'.")
                return None
        except User.DoesNotExist:
            print("Authentication failed for '"+username+"'.")
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
