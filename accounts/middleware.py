from django.contrib.auth import logout
from django.shortcuts import redirect


class BanCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            if request.user.is_banned:
                logout(request)
                return redirect("login")

        response = self.get_response(request)
        return response
