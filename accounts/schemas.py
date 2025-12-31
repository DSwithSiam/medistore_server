"""
Swagger/OpenAPI schema definitions for accounts endpoints.
Uses DRF serializers as the single source of truth - following industry best practices.
"""

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    SendOTPSerializer,
    VerifyOTPSerializer,
    VerifyResetOTPSerializer,
    ResetPasswordSerializer,
    ResendOTPSerializer,
    LogoutRequestSerializer,
    # Response serializers
    AuthResponseSerializer,
    UserResponseSerializer,
    UserListResponseSerializer,
    MessageSerializer,
    ErrorSerializer,
    OTPResponseSerializer,
    OTPVerificationResponseSerializer,
)

# ==================== Common Response Schemas ====================

error_responses = {
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Bad Request - Validation errors",
        schema=ErrorSerializer,
    ),
    status.HTTP_401_UNAUTHORIZED: openapi.Response(
        description="Unauthorized - Invalid credentials or token",
        schema=ErrorSerializer,
    ),
    status.HTTP_403_FORBIDDEN: openapi.Response(
        description="Forbidden - Insufficient permissions",
        schema=ErrorSerializer,
    ),
    status.HTTP_404_NOT_FOUND: openapi.Response(
        description="Not Found - Resource does not exist",
        schema=ErrorSerializer,
    ),
}

# JWT Bearer token security definition
bearer_auth = openapi.Parameter(
    "Authorization",
    openapi.IN_HEADER,
    description="JWT access token (format: Bearer <token>)",
    type=openapi.TYPE_STRING,
    required=True,
)

# ==================== Swagger Decorators ====================

# ==================== Swagger Decorators ====================


register_user_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Register New User",
    operation_description="""
    Register a new user account and send email verification OTP.
    Returns JWT tokens and user profile data.
    
    **Note**: Profile picture should be sent as multipart/form-data.
    """,
    request_body=UserRegistrationSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="User registered successfully",
            schema=AuthResponseSerializer,
            examples={
                "application/json": {
                    "message": "User registered successfully. Please check your email for the verification code.",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_verified": False,
                        "is_active": True,
                    },
                    "tokens": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                    "email_sent": True,
                }
            },
        ),
        **error_responses,
    },
    tags=["Authentication"],
)


login_user_swagger = swagger_auto_schema(
    method="post",
    operation_summary="User Login",
    operation_description="""
    Authenticate user with email and password.
    Returns JWT tokens and user profile data.
    """,
    request_body=UserLoginSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Login successful",
            schema=AuthResponseSerializer,
            examples={
                "application/json": {
                    "message": "Login successful",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_verified": True,
                        "is_active": True,
                    },
                    "tokens": {
                        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    },
                }
            },
        ),
        **error_responses,
    },
    tags=["Authentication"],
)


logout_user_swagger = swagger_auto_schema(
    method="post",
    operation_summary="User Logout",
    operation_description="""
    Logout user by blacklisting the refresh token.
    Requires valid JWT access token in Authorization header.
    """,
    request_body=LogoutRequestSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Logout successful",
            schema=MessageSerializer,
        ),
        **error_responses,
    },
    tags=["Authentication"],
    manual_parameters=[bearer_auth],
)


get_user_profile_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Get User Profile",
    operation_description="""
    Retrieve the authenticated user's profile information.
    Requires valid JWT access token.
    """,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="User profile retrieved",
            schema=UserResponseSerializer,
            examples={
                "application/json": {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "phone_number": "+1234567890",
                        "address": "123 Main St",
                        "profile_picture": "http://example.com/media/profile_pics/user.jpg",
                        "is_verified": True,
                        "is_active": True,
                    }
                }
            },
        ),
        **error_responses,
    },
    tags=["User Profile"],
    manual_parameters=[bearer_auth],
)


update_user_profile_swagger = swagger_auto_schema(
    methods=["put", "patch"],
    operation_summary="Update User Profile",
    operation_description="""
    Update the authenticated user's profile information.
    Supports both full update (PUT) and partial update (PATCH).
    
    **Note**: Profile picture should be sent as multipart/form-data.
    """,
    request_body=UserUpdateSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Profile updated successfully",
            schema=UserResponseSerializer,
            examples={
                "application/json": {
                    "message": "Profile updated successfully",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "is_verified": True,
                        "is_active": True,
                    },
                }
            },
        ),
        **error_responses,
    },
    tags=["User Profile"],
    manual_parameters=[bearer_auth],
)


change_password_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Change Password",
    operation_description="""
    Change the authenticated user's password.
    Requires current password for verification.
    """,
    request_body=ChangePasswordSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Password changed successfully",
            schema=MessageSerializer,
        ),
        **error_responses,
    },
    tags=["User Profile"],
    manual_parameters=[bearer_auth],
)


delete_user_swagger = swagger_auto_schema(
    method="delete",
    operation_summary="Delete User Account",
    operation_description="""
    Permanently delete the authenticated user's account.
    This action cannot be undone.
    """,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Account deleted successfully",
            schema=MessageSerializer,
        ),
        **error_responses,
    },
    tags=["User Profile"],
    manual_parameters=[bearer_auth],
)


user_list_swagger = swagger_auto_schema(
    method="get",
    operation_summary="List All Users (Admin)",
    operation_description="""
    Retrieve a list of all users.
    Requires admin/staff privileges.
    """,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Users retrieved successfully",
            schema=UserListResponseSerializer,
            examples={
                "application/json": {
                    "users": [
                        {
                            "id": 1,
                            "email": "user1@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                        },
                        {
                            "id": 2,
                            "email": "user2@example.com",
                            "first_name": "Jane",
                            "last_name": "Smith",
                        },
                    ],
                    "count": 2,
                }
            },
        ),
        **error_responses,
    },
    tags=["Admin"],
    manual_parameters=[bearer_auth],
)


get_user_by_id_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Get User by ID (Admin)",
    operation_description="""
    Retrieve a specific user's profile by ID.
    Requires admin/staff privileges.
    """,
    manual_parameters=[
        bearer_auth,
        openapi.Parameter(
            "user_id",
            openapi.IN_PATH,
            description="User ID",
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="User retrieved successfully",
            schema=UserResponseSerializer,
        ),
        **error_responses,
    },
    tags=["Admin"],
)


# ==================== OTP & Email Verification ====================


resend_otp_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Resend OTP",
    operation_description="""
    Resend OTP for email verification or password reset.
    Specify the purpose: 'verification' or 'reset'.
    """,
    request_body=ResendOTPSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="OTP sent successfully",
            schema=OTPResponseSerializer,
            examples={
                "application/json": {
                    "message": "OTP has been sent to your email for verification",
                    "email_sent": True,
                }
            },
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)


send_verification_otp_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Send Verification OTP",
    operation_description="""
    Send OTP for email verification.
    Used when user needs to verify their email address.
    """,
    request_body=SendOTPSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Verification OTP sent",
            schema=OTPResponseSerializer,
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)


verify_email_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Verify OTP",
    operation_description="""
    Verify OTP for email verification or password reset.
    The purpose field determines the verification type.
    
    - For email verification: marks user as verified
    - For password reset: allows proceeding to password reset
    """,
    request_body=VerifyResetOTPSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="OTP verified successfully",
            schema=OTPVerificationResponseSerializer,
            examples={
                "application/json": {
                    "success": True,
                    "message": "Email verified successfully",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "is_verified": True,
                    },
                }
            },
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)


send_reset_password_otp_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Send Password Reset OTP",
    operation_description="""
    Send OTP for password reset.
    User will receive an OTP code via email to reset their password.
    """,
    request_body=SendOTPSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Password reset OTP sent",
            schema=OTPResponseSerializer,
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)


verify_reset_otp_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Verify Reset OTP",
    operation_description="""
    Verify OTP for password reset.
    Must be called before reset_password endpoint.
    """,
    request_body=VerifyResetOTPSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="OTP verified, proceed to reset password",
            schema=OTPVerificationResponseSerializer,
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)


reset_password_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Reset Password",
    operation_description="""
    Reset user password with email and new password.
    OTP must be verified first using verify_otp endpoint.
    """,
    request_body=ResetPasswordSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Password reset successfully",
            schema=MessageSerializer,
            examples={"application/json": {"message": "Password reset successfully"}},
        ),
        **error_responses,
    },
    tags=["OTP & Verification"],
)
