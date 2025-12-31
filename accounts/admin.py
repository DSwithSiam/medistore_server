from django.contrib import admin
from django.contrib.admin.models import LogEntry
from accounts.models import OTP, User
from django.contrib.auth.models import Group

admin.site.unregister(Group)
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_verified", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = ("is_verified", "is_active", "is_staff")

    # Disable automatic logging to avoid FK constraint issues
    def log_addition(self, request, object, message):
        """Disable log addition"""
        pass

    def log_change(self, request, object, message):
        """Disable log change"""
        pass

    def log_deletion(self, request, object, object_repr):
        """Disable log deletion"""
        pass

    def save_model(self, request, obj, form, change):
        """Override save to handle any potential issues"""
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """Override delete to handle LogEntry foreign key constraint"""
        # Delete all LogEntry records associated with this user
        LogEntry.objects.filter(user_id=obj.pk).delete()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """Override bulk delete to handle LogEntry foreign key constraint"""
        # Delete all LogEntry records for users being deleted
        user_ids = list(queryset.values_list("pk", flat=True))
        LogEntry.objects.filter(user_id__in=user_ids).delete()
        super().delete_queryset(request, queryset)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("email", "purpose", "created_at", "expires_at", "is_used")
    search_fields = ("email", "otp_code", "purpose")
    list_filter = ("purpose", "is_used", "created_at")
    ordering = ("-created_at",)

    # Disable automatic logging to avoid FK constraint issues
    def log_addition(self, request, object, message):
        """Disable log addition"""
        pass

    def log_change(self, request, object, message):
        """Disable log change"""
        pass

    def log_deletion(self, request, object, object_repr):
        """Disable log deletion"""
        pass
