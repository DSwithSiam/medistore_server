from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.payment_list, name="payment-list"),
    path("<int:payment_id>/", views.payment_detail, name="payment-detail"),
]
