from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


payments_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Payments",
    operation_description="Retrieve Payments List",
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Payments"],
)


payment_details_swagger = swagger_auto_schema(
    method="get",
    operation_summary="Payment Details",
    operation_description="Retrieve Specific Payment Details",
    mannual_parameters=[
        openapi.Parameter(
            "payment_id",
            openapi.IN_PATH,
            description="ID of the payment to retrieve",
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(description="Successful Response"),
        status.HTTP_404_NOT_FOUND: openapi.Response(description="Payment not found"),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(description="Unauthorized"),
    },
    tags=["Payments"],
)
