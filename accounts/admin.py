from django.contrib import admin
from django.contrib.admin.models import LogEntry
from accounts.models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_verified", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = ("is_verified", "is_active", "is_staff")

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
