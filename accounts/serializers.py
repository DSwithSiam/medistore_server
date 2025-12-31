from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, OTP
from rest_framework.response import Response
from rest_framework import status


# ==================== Response Serializers ====================


class TokenSerializer(serializers.Serializer):
    """JWT token pair serializer"""

    refresh = serializers.CharField(
        help_text="JWT refresh token (valid for 24 hours)",
        read_only=True,
    )
    access = serializers.CharField(
        help_text="JWT access token (valid for 5 minutes)",
        read_only=True,
    )


class MessageSerializer(serializers.Serializer):
    """Generic message response serializer"""

    message = serializers.CharField(read_only=True)


class ErrorSerializer(serializers.Serializer):
    """Generic error response serializer"""

    error = serializers.CharField(read_only=True)


class AuthResponseSerializer(serializers.Serializer):
    """Authentication response with user, tokens, and message"""

    message = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()
    tokens = TokenSerializer(read_only=True)
    email_sent = serializers.BooleanField(
        required=False, read_only=True, help_text="Whether OTP email was sent"
    )

    def get_user(self):
        # This will be overridden with actual UserProfileSerializer data
        return {}


class UserResponseSerializer(serializers.Serializer):
    """User response with optional message"""

    message = serializers.CharField(read_only=True, required=False)
    user = serializers.SerializerMethodField()

    def get_user(self):
        return {}


class UserListResponseSerializer(serializers.Serializer):
    """User list response"""

    users = serializers.ListField(child=serializers.DictField(), read_only=True)
    count = serializers.IntegerField(read_only=True)


class OTPResponseSerializer(serializers.Serializer):
    """OTP operation response"""

    message = serializers.CharField(read_only=True)
    email_sent = serializers.BooleanField(read_only=True)


class OTPVerificationResponseSerializer(serializers.Serializer):
    """OTP verification success response"""

    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    user = serializers.DictField(required=False, read_only=True)


class LogoutRequestSerializer(serializers.Serializer):
    """Logout request body"""

    refresh_token = serializers.CharField(
        required=True, help_text="JWT refresh token to blacklist"
    )


# ==================== Request/Input Serializers ====================


class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="Email already exists."
            )
        ],
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "profile_picture",
        )

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "profile_picture",
            "is_verified",
            "is_active",
        )
        read_only_fields = ("id", "email", "is_verified", "is_active")


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "profile_picture",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)


class VerifyResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    purpose = serializers.ChoiceField(
        choices=["verification", "reset"],
        required=True,
        help_text="Purpose of OTP: 'verification' for email verification, 'reset' for password reset",
    )
