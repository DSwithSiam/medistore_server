from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard_home, name='product-list'),
    path('filter/<str:category>/', views.filter_products, name='filter-products'),
    path('search/', views.search_products, name='search-products'),
    path('request_quote/', views.request_quote, name='request-quote'),
]