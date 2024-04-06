from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from myapp.models import User


class MyTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_MYTOKEN", "")
        if token is not None:
            print("validate token==>" + token)
            users = User.objects.filter(token=token)
            if not token or len(users) == 0:
                raise exceptions.AuthenticationFailed("AUTH_FAIL")
            else:
                print('token validation passed')
        else:
            print("validate token==>token is null")
            raise exceptions.AuthenticationFailed("AUTH_FAIL")

class AirlineTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_MYTOKEN", "")
        if token is not None:
            print("Airline member validate token==>" + token)
            users = User.objects.filter(token=token)
            if not token or len(users) == 0 or users[0].user_auth != "airline_member":
                raise exceptions.AuthenticationFailed("AUTH_FAIL")
            else:
                print('token validation passed')
        else:
            print("Airline member validate token==>token is null")
            raise exceptions.AuthenticationFailed("AUTH_FAIL")

class AirportTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_MYTOKEN", "")
        if token is not None:
            print("Airport member validate token==>" + token)
            users = User.objects.filter(token=token)
            if not token or len(users) == 0 or users[0].user_auth != "airport_member":
                raise exceptions.AuthenticationFailed("AUTH_FAIL")
            else:
                print('token validation passed')
        else:
            print("Airport member validate token==>token is null")
            raise exceptions.AuthenticationFailed("AUTH_FAIL")

class AdminTokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_MYTOKEN", "")
        if token is not None:
            print("Admin validate token==>" + token)
            users = User.objects.filter(token=token)
            if not token or len(users) == 0 or users[0].user_auth != "admin":
                raise exceptions.AuthenticationFailed("AUTH_FAIL")
            else:
                print('token validation passed')
        else:
            print("Admin validate token==>token is null")
            raise exceptions.AuthenticationFailed("AUTH_FAIL")