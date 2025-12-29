from django.contrib import admin

from payments.models import BKashPayment, Payment


# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_method", "amount", "status", "created_at")
    list_filter = ("payment_method", "status", "created_at")
    search_fields = ("user__username", "payment_method", "status")


@admin.register(BKashPayment)
class BKashPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "payment",
        "bkash_payment_id",
        "trx_id",
        "merchant_invoice_number",
        "status",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "payment__user__username",
        "bkash_payment_id",
        "trx_id",
        "merchant_invoice_number",
        "status",
    )
