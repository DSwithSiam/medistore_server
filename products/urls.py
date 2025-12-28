from django.urls import path
from . import views

urlpatterns = [
    path('all_products/', views.product_list, name='product-list'),
    path('create/', views.product_create, name='product-create'),
    path('<slug:product_ref>/', views.product_detail, name='product-detail'),
    path('<slug:product_ref>/update/', views.product_update, name='product-update'),
    path('<slug:product_ref>/delete/', views.product_delete, name='product-delete'),
]