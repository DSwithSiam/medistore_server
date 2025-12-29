from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from .models import User, OTP
from .utils import send_otp_email
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer,
    ResendOTPSerializer,
)
from .schemas import (
    register_user_swagger,
    login_user_swagger,
    logout_user_swagger,
    get_user_profile_swagger,
    update_user_profile_swagger,
    change_password_swagger,
)


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@register_user_swagger
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate OTP for email verification
        otp = OTP.create_otp(user.email, "verification")

        # Send OTP via email
        email_sent, email_message = send_otp_email(
            user.email, otp.otp_code, "verification"
        )

        tokens = get_tokens_for_user(user)
        user_data = UserProfileSerializer(user).data

        response_message = "User registered successfully. "
        if email_sent:
            response_message += "Please check your email for the verification code."
        else:
            response_message += f"Unable to send email. {email_message}"

        return Response(
            {
                "message": response_message,
                "user": user_data,
                "tokens": tokens,
                "email_sent": email_sent,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_user_swagger
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    """Login user and return JWT tokens"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(email=email, password=password)
        if not user:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_active:
            update_last_login(None, user)
            tokens = get_tokens_for_user(user)
            user_data = UserProfileSerializer(user).data

            return Response(
                {
                    "message": "Login successful",
                    "user": user_data,
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Account is disabled"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@logout_user_swagger
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logout user by blacklisting refresh token"""
    refresh_token = request.data.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    except TokenError:
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
        )


@get_user_profile_swagger
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    serializer = UserProfileSerializer(request.user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@update_user_profile_swagger
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """Update current user profile"""
    serializer = UserUpdateSerializer(
        request.user, data=request.data, partial=request.method == "PATCH"
    )
    if serializer.is_valid():
        serializer.save()
        user_data = UserProfileSerializer(request.user).data
        return Response(
            {"message": "Profile updated successfully", "user": user_data},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@change_password_swagger
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """Get all users (admin only)"""
    if not request.user.is_staff:
        return Response(
            {"error": "Permission denied. Admin access required."},
            status=status.HTTP_403_FORBIDDEN,
        )

    users = User.objects.all()
    serializer = UserProfileSerializer(users, many=True)
    return Response(
        {"users": serializer.data, "count": users.count()}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, user_id):
    """Get user by ID (admin only)"""
    if not request.user.is_staff:
        return Response(
            {"error": "Permission denied. Admin access required."},
            status=status.HTTP_403_FORBIDDEN,
        )

    user = get_object_or_404(User, id=user_id)
    serializer = UserProfileSerializer(user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    """Delete current user account"""
    user = request.user
    user.delete()
    return Response(
        {"message": "Account deleted successfully"}, status=status.HTTP_200_OK
    )


# OTP and Email Verification Endpoints


@api_view(["POST"])
@permission_classes([AllowAny])
def resend_otp(request):
    """Resend OTP for verification or password reset"""
    serializer = ResendOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        purpose = serializer.validated_data["purpose"]

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if already verified for verification purpose
        if purpose == "verification" and user.is_verified:
            return Response(
                {"message": "Email is already verified"}, status=status.HTTP_200_OK
            )

        # Generate OTP
        otp = OTP.create_otp(email, purpose)

        # Send OTP via email
        email_sent, email_message = send_otp_email(email, otp.otp_code, purpose)

        purpose_text = "verification" if purpose == "verification" else "password reset"

        if email_sent:
            response_msg = f"OTP has been sent to your email for {purpose_text}"
        else:
            response_msg = f"Unable to send email. {email_message}"

        return Response(
            {
                "message": response_msg,
                "email_sent": email_sent,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_verification_otp(request):
    """Send OTP for email verification"""
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if user.is_verified:
            return Response(
                {"message": "Email is already verified"}, status=status.HTTP_200_OK
            )

        # Generate OTP
        otp = OTP.create_otp(email, "verification")

        # Send OTP via email
        email_sent, email_message = send_otp_email(email, otp.otp_code, "verification")

        if email_sent:
            response_msg = "Verification code has been sent to your email"
        else:
            response_msg = f"Unable to send email. {email_message}"

        return Response(
            {"message": response_msg, "email_sent": email_sent},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_email_otp(request):
    """Verify email using OTP"""
    serializer = VerifyOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Find valid OTP
        try:
            otp = OTP.objects.filter(
                email=email, otp_code=otp_code, purpose="verification", is_used=False
            ).latest("created_at")

            if not otp.is_valid():
                return Response(
                    {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Mark OTP as used and verify user
            otp.is_used = True
            otp.save()

            user.is_verified = True
            user.save()

            return Response(
                {
                    "message": "Email verified successfully",
                    "user": UserProfileSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )

        except OTP.DoesNotExist:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def send_password_reset_otp(request):
    """Send OTP for password reset"""
    serializer = SendOTPSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]

        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Generate OTP
        otp = OTP.create_otp(email, "reset")

        # Send OTP via email
        email_sent, email_message = send_otp_email(email, otp.otp_code, "reset")

        if email_sent:
            response_msg = "Password reset code has been sent to your email"
        else:
            response_msg = f"Unable to send email. {email_message}"

        return Response(
            {"message": response_msg, "email_sent": email_sent},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_with_otp(request):
    """Reset password using OTP"""
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp_code"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Find valid OTP
        try:
            otp = OTP.objects.filter(
                email=email, otp_code=otp_code, purpose="reset", is_used=False
            ).latest("created_at")

            if not otp.is_valid():
                return Response(
                    {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Mark OTP as used and reset password
            otp.is_used = True
            otp.save()

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password reset successfully"}, status=status.HTTP_200_OK
            )

        except OTP.DoesNotExist:
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
