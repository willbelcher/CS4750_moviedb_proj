from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import db_utils

class MovieDBBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = db_utils.get_user(username)

        if user is not None:
            if user.check_password(password):
                return user

        return None 
    
    def get_user(self, user_id):
        return db_utils.get_user(user_id)