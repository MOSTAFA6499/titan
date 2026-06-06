from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Organization

class CustomUserAdmin(UserAdmin):
    """تنظیمات نمایش کاربر در پنل ادمین"""
    
    list_display = ('username', 'get_full_name', 'phone', 'role', 'organization', 'is_active')
    list_filter = ('role', 'organization', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone', 'guardian_phone', 'role', 'organization', 'avatar')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات اضافی', {'fields': ('phone', 'guardian_phone', 'role', 'organization', 'first_name', 'last_name')}),
    )

class OrganizationAdmin(admin.ModelAdmin):
    """تنظیمات نمایش سازمان در پنل ادمین"""
    
    list_display = ('name', 'slug', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(User, CustomUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
