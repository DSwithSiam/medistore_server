from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


all_products_swagger = swagger_auto_schema(
    method="get",
    operation_summary="All Products",
    operation_description="Retrieve All Products",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Products"],
)

product_create_swagger = swagger_auto_schema(
    method="post",
    operation_summary="Create Product",
    operation_description="Create a New Product",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product name"
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Product category",
                enum=[
                    "hospital_equipment",
                    "blood_pressure",
                    "accessories",
                    "personal",
                ],
            ),
            "used_for": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="What the product is used for",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product description"
            ),
            "price": openapi.Schema(
                type=openapi.TYPE_NUMBER, description="Product price"
            ),
            "discount": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="Discount percentage",
                default=0.00,
            ),
            "sku": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Stock Keeping Unit (unique identifier)",
            ),
            "stock_quantity": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Stock quantity"
            ),
            "product_image": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_BINARY,
                description="Product image file",
            ),
            "additional_info": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="Additional product information (tabular data)",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "key": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Information key/label",
                            example="Weight",
                        ),
                        "value": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Information value",
                            example="2.5 kg",
                        ),
                    },
                    required=["key", "value"],
                ),
            ),
        },
        required=[
            "name",
            "category",
            "used_for",
            "description",
            "price",
            "sku",
            "stock_quantity",
        ],
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Product created successfully"
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description="Invalid input"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Products"],
)

product_detail_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Product Detail",
    operation_description="Retrieve Product Details by product_ref",
    manual_parameters=[
        openapi.Parameter(
            "product_ref",
            openapi.IN_PATH,
            description="Reference ID of the product",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Product not found"),
    },
    tags=["Products"],
)

update_product_swagger = swagger_auto_schema(
    method="patch",
    operation_summary="Update Product",
    operation_description="Update an Existing Product by product_ref",
    manual_parameters=[
        openapi.Parameter(
            "product_ref",
            openapi.IN_PATH,
            description="Reference ID of the product",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product name"
            ),
            "category": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Product category",
                enum=[
                    "hospital_equipment",
                    "blood_pressure",
                    "accessories",
                    "personal",
                ],
            ),
            "used_for": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="What the product is used for",
            ),
            "description": openapi.Schema(
                type=openapi.TYPE_STRING, description="Product description"
            ),
            "price": openapi.Schema(
                type=openapi.TYPE_NUMBER, description="Product price"
            ),
            "discount": openapi.Schema(
                type=openapi.TYPE_NUMBER,
                description="Discount percentage",
                default=0.00,
            ),
            "sku": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Stock Keeping Unit (unique identifier)",
            ),
            "stock_quantity": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="Stock quantity"
            ),
            "product_image": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_BINARY,
                description="Product image file",
            ),
            "additional_info": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description="Additional product information (tabular data)",
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "key": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Information key/label",
                            example="Weight",
                        ),
                        "value": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Information value",
                            example="2.5 kg",
                        ),
                    },
                    required=["key", "value"],
                ),
            ),
        },
    ),
    tags=["Products"],
)

delete_product_swagger = swagger_auto_schema(
    method="delete",
    operation_summary="Delete Product",
    operation_description="Delete a Product by product_ref",
    manual_parameters=[
        openapi.Parameter(
            "product_ref",
            openapi.IN_PATH,
            description="Reference ID of the product",
            type=openapi.TYPE_STRING,
            required=True,
        )
    ],
    responses={
        status.HTTP_204_NO_CONTENT: openapi.Response(description="Product deleted"),
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Product not found"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Products"],
)
