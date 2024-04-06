from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from myapp.serializers import CustomTokenRefreshSerializer, CustomTokenObtainPairSerializer, CustomTokenVerifySerializer


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenVerifyView(TokenVerifyView):
    serializer_class = CustomTokenVerifySerializer