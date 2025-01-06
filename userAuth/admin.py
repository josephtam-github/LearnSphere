from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_email_verified', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)