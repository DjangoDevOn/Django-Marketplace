from django.contrib import admin
from .models import *
from website.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Notification Settings
admin.site.register(UserNotificationSettings)

# FAQ
admin.site.register(Faq)
admin.site.register(FaqCat)

# Selling Options
admin.site.register(Selling)


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('useralias', 'email', 'password', 'profile_photo', 'first_name', 'last_name', 'company_name', 'business_street_address', 'business_street_address2','city','state','zip_code','company_phone_number', 'buyer_account', 'selling',)}),
        ('Permissions', {'fields': ('is_admin', 'is_staff','is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
