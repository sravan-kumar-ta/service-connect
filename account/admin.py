from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from account.models import OTP

User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'is_verified': 'Verification status',
            'is_active': 'Active',
            'is_staff': 'Staff status'
        }
        help_texts = {
            'is_verified': 'Indicates whether the user\'s email address has been verified through OTP.'
                           'Uncheck this to treat the user as unverified.',
            'is_active': 'Designates whether this user should be treated as active. '
                         'Unselect this instead of deleting accounts.',
            'is_staff': 'Designates whether the user can log into this admin site.'
        }


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        (_('Personal info'), {'fields': ('email', 'password',)}),
        (_('Permissions'), {'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser',)}),
    )

    list_display = ('id', 'email', 'is_verified', 'is_staff')
    list_filter = ('is_verified', 'is_staff', 'is_active')
    filter_horizontal = ()
    ordering = ("-id",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(OTP)

# sample test
