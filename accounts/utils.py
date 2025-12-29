from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def is_email_configured():
    """Check if email is properly configured"""
    return bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)


def send_otp_email(email, otp_code, purpose):
    """
    Send OTP email to user

    Args:
        email: Recipient email address
        otp_code: The OTP code to send
        purpose: 'verification' or 'reset'

    Returns:
        tuple: (success: bool, message: str)
    """
    # Check if email is configured
    if not is_email_configured():
        logger.warning(
            "Email not configured. Please set EMAIL and PASSWORD in .env file"
        )
        return False, "Email service not configured. Please contact administrator."

    if purpose == "verification":
        subject = "Verify Your Email - Medistore"
        message = f"""
Hello,

Thank you for registering with Medistore!

Your email verification code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Medistore Team
        """
    else:  # reset
        subject = "Password Reset Request - Medistore"
        message = f"""
Hello,

You requested to reset your password for your Medistore account.

Your password reset code is: {otp_code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email and your password will remain unchanged.

Best regards,
Medistore Team
        """

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return True, "Email sent successfully"
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error sending email to {email}: {error_msg}")

        # Provide user-friendly error messages
        if "Authentication" in error_msg or "530" in error_msg:
            return (
                False,
                "Email authentication failed. Please configure email credentials.",
            )
        elif "Connection" in error_msg:
            return False, "Unable to connect to email server."
        else:
            return False, "Failed to send email. Please try again later."
