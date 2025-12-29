from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, BKashPayment
from .serializers import PaymentSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_list(request):
    """Get all payments (admin only) or current user's payments"""
    if request.user.is_staff:
        payments = (
            Payment.objects.all()
            .select_related("user", "bkash")
            .order_by("-created_at")
        )
    else:
        payments = (
            Payment.objects.filter(user=request.user)
            .select_related("bkash")
            .order_by("-created_at")
        )

    serializer = PaymentSerializer(payments, many=True)
    return Response({"payments": serializer.data, "count": payments.count()})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_detail(request, payment_id):
    """Get specific payment details"""
    try:
        if request.user.is_staff:
            payment = Payment.objects.select_related("user", "bkash").get(id=payment_id)
        else:
            payment = Payment.objects.select_related("bkash").get(
                id=payment_id, user=request.user
            )
    except Payment.DoesNotExist:
        return Response(
            {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = PaymentSerializer(payment)
    return Response({"payment": serializer.data})
