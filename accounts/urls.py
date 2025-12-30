from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication endpoints
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User profile endpoints
    path("profile/", views.get_user_profile, name="user_profile"),
    path("profile/update/", views.update_user_profile, name="update_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("delete-account/", views.delete_user_account, name="delete_account"),
    # Admin endpoints
    path("users/", views.get_all_users, name="all_users"),
    path("users/<int:user_id>/", views.get_user_by_id, name="user_by_id"),
    # OTP and Email Verification endpoints
    path("resend-otp/", views.resend_otp, name="resend_otp"),
    path(
        "send-verification-otp/",
        views.send_verification_otp,
        name="send_verification_otp",
    ),
    path("verify-email/", views.verify_email_otp, name="verify_email"),
    path("send-reset-otp/", views.send_password_reset_otp, name="send_reset_otp"),
    path("verify-reset-otp/", views.verify_reset_otp, name="verify_reset_otp"),
    path("reset-password/", views.reset_password_with_otp, name="reset_password"),
]
