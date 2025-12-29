from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


# ==================== Request Body Schemas ====================

register_request_schema = openapi.Schema(
    method = 'POST',
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description='User email address (must be unique)',
            example='user@example.com'
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_PASSWORD,
            description='User password (will be hashed)',
            example='SecurePassword123!'
        ),
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User first name',
            example='John'
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User last name',
            example='Doe'
        ),
        'phone_number': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User phone number',
            example='+1234567890'
        ),
        'address': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User address',
            example='123 Main St, City, State 12345'
        ),
        'profile_picture': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description='User profile picture (image file)'
        ),
    }
)

login_request_schema = openapi.Schema(
    method = 'POST',
    type=openapi.TYPE_OBJECT,
    required=['email', 'password'],
    properties={
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description='User email address',
            example='user@example.com'
        ),
        'password': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_PASSWORD,
            description='User password',
            example='SecurePassword123!'
        ),
    }
)

logout_request_schema = openapi.Schema(
    method = 'POST',
    type=openapi.TYPE_OBJECT,
    required=['refresh_token'],
    properties={
        'refresh_token': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT refresh token to blacklist',
            example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        ),
    }
)

update_profile_request_schema = openapi.Schema(
    method = 'PUT/PATCH',
    type=openapi.TYPE_OBJECT,
    properties={
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User first name',
            example='John'
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User last name',
            example='Doe'
        ),
        'phone_number': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User phone number',
            example='+1234567890'
        ),
        'address': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User address',
            example='123 Main St, City, State 12345'
        ),
        'profile_picture': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_BINARY,
            description='User profile picture (image file)'
        ),
    }
)

change_password_request_schema = openapi.Schema(
    method = 'POST',
    type=openapi.TYPE_OBJECT,
    required=['old_password', 'new_password'],
    properties={
        'old_password': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_PASSWORD,
            description='Current user password',
            example='OldPassword123!'
        ),
        'new_password': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_PASSWORD,
            description='New password (must be different from old password)',
            example='NewPassword123!'
        ),
    }
)


# ==================== Response Schemas ====================

user_profile_schema = openapi.Schema(
    method = 'GET',
    type=openapi.TYPE_OBJECT,
    properties={
        'id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='User unique identifier',
            example=1
        ),
        'email': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            description='User email address',
            example='user@example.com'
        ),
        'first_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User first name',
            example='John'
        ),
        'last_name': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User last name',
            example='Doe'
        ),
        'phone_number': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User phone number',
            example='+1234567890'
        ),
        'address': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='User address',
            example='123 Main St, City, State 12345'
        ),
        'profile_picture': openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_URI,
            description='URL to user profile picture',
            example='http://example.com/media/profile_pics/user_1.jpg'
        ),
        'is_verified': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='Whether user email is verified',
            example=False
        ),
        'is_active': openapi.Schema(
            type=openapi.TYPE_BOOLEAN,
            description='Whether user account is active',
            example=True
        ),
    }
)

tokens_schema = openapi.Schema(
    method = 'POST',
    type=openapi.TYPE_OBJECT,
    properties={
        'refresh': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT refresh token (valid for 24 hours)',
            example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        ),
        'access': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='JWT access token (valid for 5 minutes)',
            example='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        ),
    }
)

register_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='User registered successfully'
        ),
        'user': user_profile_schema,
        'tokens': tokens_schema,
    }
)

login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='Login successful'
        ),
        'user': user_profile_schema,
        'tokens': tokens_schema,
    }
)

profile_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'user': user_profile_schema,
    }
)

update_profile_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='Profile updated successfully'
        ),
        'user': user_profile_schema,
    }
)

success_message_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'message': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Success message',
            example='Operation successful'
        ),
    }
)

error_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'error': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='Error message',
            example='Invalid credentials'
        ),
    }
)

validation_error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'field_name': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(type=openapi.TYPE_STRING),
            description='Array of validation error messages for the field',
            example=['This field is required.']
        ),
    }
)


# ==================== Swagger Decorators ====================

register_user_swagger = swagger_auto_schema(
    methods=['post'],
    operation_id='accounts_register',
    operation_description='Register a new user account. Email must be unique and password will be securely hashed.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['email', 'password'],
        properties={
            'email': register_request_schema.properties['email'],
            'password': register_request_schema.properties['password'],
            'first_name': register_request_schema.properties['first_name'],
            'last_name': register_request_schema.properties['last_name'],
            'phone_number': register_request_schema.properties['phone_number'],
            'address': register_request_schema.properties['address'],
            'profile_picture': register_request_schema.properties['profile_picture'],
        }
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description='User successfully registered',
            schema=register_response_schema
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Validation error (e.g., invalid email, email already exists, weak password)',
            schema=validation_error_schema
        ),
    },
    tags=['Authentication'],
)

login_user_swagger = swagger_auto_schema(
    methods=['post'],
    operation_id='accounts_login',
    operation_description='Authenticate user with email and password. Returns JWT tokens for subsequent API calls.',
    request_body=login_request_schema,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Login successful',
            schema=login_response_schema
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Invalid credentials or account disabled',
            schema=error_response_schema
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Validation error',
            schema=validation_error_schema
        ),
    },
    tags=['Authentication'],
)

logout_user_swagger = swagger_auto_schema(
    methods=['post'],
    operation_id='accounts_logout',
    operation_description='Logout user by blacklisting the refresh token. The refresh token will no longer be usable after logout.',
    request_body=logout_request_schema,
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Logout successful',
            schema=success_message_schema
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Refresh token required or invalid',
            schema=error_response_schema
        ),
    },
    tags=['Authentication'],
)

get_user_profile_swagger = swagger_auto_schema(
    methods=['get'],
    operation_id='accounts_profile_retrieve',
    operation_description='Retrieve the current authenticated user profile information.',
    security=[{'Bearer': []}],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='User profile retrieved successfully',
            schema=profile_response_schema
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Authentication credentials were not provided or are invalid',
            schema=error_response_schema
        ),
    },
    tags=['User Profile'],
)

update_user_profile_swagger = swagger_auto_schema(
    methods=['put', 'patch'],
    operation_id='accounts_profile_update',
    operation_description='Update the current authenticated user profile. Supports both PUT (full update) and PATCH (partial update) methods.',
    request_body=update_profile_request_schema,
    security=[{'Bearer': []}],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Profile updated successfully',
            schema=update_profile_response_schema
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Validation error',
            schema=validation_error_schema
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Authentication credentials were not provided or are invalid',
            schema=error_response_schema
        ),
    },
    tags=['User Profile'],
)

change_password_swagger = swagger_auto_schema(
    methods=['post'],
    operation_id='accounts_change_password',
    operation_description='Change the current authenticated user password. Old password must be verified.',
    request_body=change_password_request_schema,
    security=[{'Bearer': []}],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description='Password changed successfully',
            schema=success_message_schema
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description='Validation error (e.g., old password incorrect)',
            schema=validation_error_schema
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description='Authentication credentials were not provided or are invalid',
            schema=error_response_schema
        ),
    },
    tags=['User Profile'],
)
