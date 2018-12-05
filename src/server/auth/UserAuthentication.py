from server.models.User import User

class UserAuthentication:
    def authenticate(self, request, username=None, password=None):
        # Checks if it is a valid user
        print("Auth user: "+username+" password: "+password)

        try:
            user = User.objects.get(username=username, password=password)
            print("auth success")
            return user
        except User.DoesNotExist:
            print("auth failed")
            return None

    def get_user(user_id):
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
