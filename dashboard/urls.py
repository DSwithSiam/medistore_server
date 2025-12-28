from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.dashboard_home, name='product-list'),
]