from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="MediStore API",
        default_version="v1",
        description="--",
        terms_of_service="--",
        contact=openapi.Contact(email="masipulislam@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/dashboard/", include("dashboard.urls")),
    path("api/v1/payments/", include("payments.urls")),
    path("api/v1/products/", include("products.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
