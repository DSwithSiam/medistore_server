
from django.contrib import admin
from django.urls import path, include   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/v1/products/', include('products.urls')),
]
