from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/  -- creates a citizen account and logs them in."""

    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, **_tokens_for(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/auth/login/  -- body: {"email": "...", "password": "..."}"""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response({"user": UserSerializer(user).data, **_tokens_for(user)})


class MeView(generics.RetrieveAPIView):
    """GET /api/auth/me/  -- returns the logged-in user (citizen or authority)."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
