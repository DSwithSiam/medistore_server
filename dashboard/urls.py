from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard_home, name='product-list'),
    path('filter/<str:category>/', views.filter_products, name='filter-products'),
    path('search/', views.search_products, name='search-products'),
    path('request_quote/', views.request_quote, name='request-quote'),
    path('quotes/', views.get_quotes, name='get-quotes'),
    # Cart endpoints
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/add/', views.cart_add_item, name='cart-add-item'),
    path('cart/items/<int:item_id>/', views.cart_update_item, name='cart-update-item'),
    path('cart/items/<int:item_id>/delete/', views.cart_delete_item, name='cart-delete-item'),
]