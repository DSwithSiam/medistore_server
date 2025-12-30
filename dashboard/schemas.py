from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


home_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Dashboard Home",
    operation_description="Retrieve Discounted and Latest Products",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

search_products_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Search Products",
    operation_description="Search Products by Name or Category",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "query": openapi.Schema(
                type=openapi.TYPE_STRING, description="Search query string"
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_STRING, description="Category to filter products"
            ),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

filtered_products_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Filtered Products",
    operation_description="Retrieve Products Filtered by Category",
    manual_parameters=[
        openapi.Parameter(
            "category",
            openapi.IN_PATH,
            description="Category to filter products",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

add_to_cart_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Add to Cart",
    operation_description="Add a Product to the User's Cart",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "product_ref": openapi.Schema(
                type=openapi.TYPE_STRING, description="Reference ID of the product"
            ),
            "quantity": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Quantity of the product to add"
            ),
        },
        required=["product_ref", "quantity"],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(description="Product added to cart"),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

update_cart_item_swagger = swagger_auto_schema(
    method="patch",
    operation_summary="Update Cart Item",
    operation_description="Update the Quantity of a Cart Item",
    manual_parameters=[
        openapi.Parameter(
            "item_id",
            openapi.IN_PATH,
            description="ID of the cart item to update",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "quantity": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="New quantity for the cart item"
            ),
        },
        required=["quantity"],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(description="Cart item updated"),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input"),
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Cart item not found"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

delete_cart_item_swagger = swagger_auto_schema(
    method="delete",
    operation_summary="Delete Cart Item",
    operation_description="Delete an Item from the User's Cart",
    manual_parameters=[
        openapi.Parameter(
            "item_id",
            openapi.IN_PATH,
            description="ID of the cart item to delete",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(description="Cart item deleted"),
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Cart item not found"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

clear_cart_swagger = swagger_auto_schema(
    method="delete",
    operation_summary="Clear Cart",
    operation_description="Remove All Items from the User's Cart",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Cart cleared"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

view_cart_swagger = swagger_auto_schema(
    method="get",
    operation_summary="View Cart",
    operation_description="Retrieve the User's Cart Details",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

order_history_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Order History",
    operation_description="Retrieve the User's Order History",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

request_quotes_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Request Quotes",
    operation_description="Submit a Quote Request for Products",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "first_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="First name of the requester"
            ),
            "last_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Last name of the requester"
            ),
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Email of the requester",
            ),
            "phone_number": openapi.Schema(
                type=openapi.TYPE_STRING, description="Phone number of the requester"
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Additional description"
            ),
        },
        required=["first_name", "last_name", "email", "phone_number", "description"],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(description="Quote request submitted"),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

get_quotes_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Get Quotes",
    operation_description="Retrieve the User's Quote Requests",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

add_to_wishlist_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Add to Wishlist",
    operation_description="Add a Product to the User's Wishlist",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "product_ref": openapi.Schema(
                type=openapi.TYPE_STRING, description="Reference ID of the product"
            ),
        },
        required=["product_ref"],
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(description="Product added to wishlist"),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)

view_wishlist_swagger = swagger_auto_schema(
    method="get",
    operation_summary="View Wishlist",
    operation_description="Retrieve the User's Wishlist",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Dashboard"],
)
