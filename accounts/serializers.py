"""Serializers for the auth boundary: registration, login and the current user."""
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Public shape of a user — never exposes the password."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name"]


class RegisterSerializer(serializers.ModelSerializer):
    """Validates sign-up input and creates a user with a properly hashed password."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "password"]

    def validate_password(self, value):
        # Run Django's configured password validators (length, common, numeric...).
        validate_password(value)
        return value

    def create(self, validated_data):
        # create_user hashes the password; never store it in plain text.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Checks an email/password pair and returns the authenticated user."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        # Our USERNAME_FIELD is 'email', so authenticate() receives it as `username`.
        user = authenticate(username=attrs["email"], password=attrs["password"])
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs
