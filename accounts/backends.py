from django.contrib.auth.backends import ModelBackend

class CustomAuthBackend(ModelBackend):

    def user_can_authenticate(self, user):
        is_valid = super().user_can_authenticate(user)
        return is_valid and not user.is_banned
