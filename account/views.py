from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers
from .models import Token

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class LoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):
        ser = serializers.UserSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            user = get_user_model().objects.get(
                username=ser.validated_data.get("username"),
            )

            if not user.check_password(ser.validated_data.get("password")):
                raise

        except Exception as e:
            return Response(
                {
                    "msg": "No active account found with the given credentials",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            # Check for user has already a token
            user_ip = request.META.get("REMOTE_ADDR", None)
            if user_ip:
                token = Token.get_user_token(user=user, ip_address=str(user_ip))
                return Response(
                    {
                        "username": user.username,
                        "token": str(token.token),
                        "expired": token.expired,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "err": "Invalid ip address",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )


class MeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({"username": request.user.username}, status=status.HTTP_200_OK)
