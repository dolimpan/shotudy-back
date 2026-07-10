# api/views/google_login_view.py

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from api.models.user import User
from rest_framework.permissions import AllowAny

GOOGLE_CLIENT_ID = "766073217846-787gbcek1th8gdk7fvltcrehg43vae66.apps.googleusercontent.com"


class GoogleLoginView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        token = request.data.get("token")

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                GOOGLE_CLIENT_ID
            )

            email = idinfo["email"]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "nickname": email.split("@")[0]
                }
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })

        except Exception:
            return Response(
                {"error": "Invalid google token"},
                status=status.HTTP_400_BAD_REQUEST
            )