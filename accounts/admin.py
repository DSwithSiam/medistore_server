from django.contrib import admin
from accounts.models import User
from django.contrib.auth.models import Group

admin.site.unregister(Group)
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)