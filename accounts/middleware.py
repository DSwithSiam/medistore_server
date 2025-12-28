from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .models import User


class JWTAuthenticationMiddleware:
    """
    Middleware to authenticate users using Simple JWT tokens
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        # Skip authentication for auth endpoints
        if request.path.startswith("/api/v1/auth/"):
            return self.get_response(request)

        # Get token from Authorization header
        auth_header = request.headers.get("Authorization", "")

        if auth_header.startswith("Bearer "):
            try:
                # Use Simple JWT's authentication
                validated_token = self.jwt_authentication.get_validated_token(
                    auth_header.split(" ")[1]
                )
                user = self.jwt_authentication.get_user(validated_token)
                request.user = user
            except (InvalidToken, TokenError):
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        return response
