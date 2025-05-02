from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import SignupForm, EditInfoForm

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'userType', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'userType')
    ordering = ('email',)
    search_fields = ('email', 'name')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'userType', 'firstNumber', 'middleNumber', 'lastNumber', 'postcode', 'address', 'detailAddress', 'extraAddress')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('date_joined',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    add_permissions = ('can_add_user', 'can_change_user', 'can_delete_user', 'can_view_user')

admin.site.register(CustomUser, CustomUserAdmin)