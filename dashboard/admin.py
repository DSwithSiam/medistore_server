from django.contrib import admin

from dashboard.models import RequestQuote

# Register your models here.
@admin.register(RequestQuote)
class RequestQuoteAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number', 'description')
    list_filter = ('created_at',)
