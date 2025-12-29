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


def get_tokens_for_user(user):
    """Generate JWT tokens for user"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Generate OTP for email verification
        otp = OTP.create_otp(user.email, "verification")

        tokens = get_tokens_for_user(user)
        user_data = UserProfileSerializer(user).data

        return Response(
            {
                "message": "User registered successfully. Please verify your email.",
                "user": user_data,
                "tokens": tokens,
                "otp": otp.otp_code,  # Demo: returning OTP in response
                "otp_expires_in": "10 minutes",
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get current user profile"""
    serializer = UserProfileSerializer(request.user)
    return Response({"user": serializer.data}, status=status.HTTP_200_OK)


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

        purpose_text = "verification" if purpose == "verification" else "password reset"
        return Response(
            {
                "message": f"OTP resent successfully for {purpose_text}",
                "otp": otp.otp_code,  # Demo: returning OTP in response
                "expires_in": "10 minutes",
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

        return Response(
            {
                "message": "OTP sent successfully",
                "otp": otp.otp_code,  # Demo: returning OTP in response
                "expires_in": "10 minutes",
            },
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

        return Response(
            {
                "message": "Password reset OTP sent successfully",
                "otp": otp.otp_code,  # Demo: returning OTP in response
                "expires_in": "10 minutes",
            },
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
