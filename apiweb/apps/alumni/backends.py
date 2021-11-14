from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        User = get_user_model()
        try:
            validate_email(username)
            valid_email = True
        except ValidationError:
            valid_email = False

        if valid_email:
            kwargs = {"email": username}
        else:
            kwargs = {"username": username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
