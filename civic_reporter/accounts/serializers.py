from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import AuthorityProfile, User


class RegisterSerializer(serializers.ModelSerializer):
    """Citizen self-registration. Authority accounts are created separately
    (e.g. via Django admin or an internal endpoint) -- see AuthorityProfile."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "area", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    is_authority = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "area",
            "trust_score",
            "verified_reports",
            "false_reports",
            "is_authority",
        ]
        read_only_fields = ["trust_score", "verified_reports", "false_reports"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("This account has been disabled.")
        attrs["user"] = user
        return attrs


class AuthorityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorityProfile
        fields = ["id", "user", "department", "area"]
