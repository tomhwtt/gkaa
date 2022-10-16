from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'name','is_staff', 'is_active',)
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('name','email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser','groups','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email','name')
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
