from django.db import models

# Create your models here.


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("bkash", "Bkash"),
        ("cod", "Cash on Delivery"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("success", "Success"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="payments"
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.payment_method} - {self.status}"


class BKashPayment(models.Model):
    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, related_name="bkash"
    )

    bkash_payment_id = models.CharField(max_length=100, null=True, blank=True)
    trx_id = models.CharField(max_length=100, null=True, blank=True)

    merchant_invoice_number = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        max_length=30,
        choices=[
            ("created", "Created"),
            ("executed", "Executed"),
            ("success", "Success"),
            ("failed", "Failed"),
        ],
        default="created",
    )

    gateway_response = models.JSONField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"BKash Payment for Payment #{self.payment.id} - {self.status}"

    class Meta:
        verbose_name = "BKash Payment"
        verbose_name_plural = "BKash Payments"