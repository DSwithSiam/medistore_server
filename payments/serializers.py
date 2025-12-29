from rest_framework import serializers
from .models import Payment, BKashPayment


class BKashPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BKashPayment
        fields = [
            "id",
            "bkash_payment_id",
            "trx_id",
            "merchant_invoice_number",
            "status",
            "gateway_response",
            "error_message",
            "created_at",
        ]
        read_only_fields = fields


class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    user_name = serializers.SerializerMethodField()
    bkash = BKashPaymentSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "user_email",
            "user_name",
            "payment_method",
            "amount",
            "status",
            "created_at",
            "bkash",
        ]
        read_only_fields = fields

    def get_user_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
