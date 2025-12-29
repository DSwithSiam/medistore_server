from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User, OTP
from rest_framework.response import Response
from rest_framework import status


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

<<<<<<< HEAD
    if User.objects.filter(email=email).exists():
        raise Response(
            {"message": "User with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

=======
>>>>>>> siam
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


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_code = serializers.CharField(required=True, max_length=6, min_length=6)
    new_password = serializers.CharField(required=True, write_only=True)


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    purpose = serializers.ChoiceField(choices=["verification", "reset"], required=True)
