from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from rest_framework import serializers

User = get_user_model()
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'nickname', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')  # 관리자 여부, 활성화 여부
    search_fields = ('email', 'nickname', 'phone_number')  # 검색 필드

    readonly_fields = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('user_info', {'fields': ('nickname', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    ordering = ('email',)