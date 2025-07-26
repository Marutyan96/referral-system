from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code', 'activated_invite_code', 'created_at')
    search_fields = ('phone_number', 'invite_code')
    list_filter = ('created_at',)