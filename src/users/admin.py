import logging

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from users.models import CustomUser, UserRoleEnum

logger = logging.getLogger(__name__)


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users.

    Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput
    )

    class Meta:
        model = CustomUser
        fields = ["email", 'first_name', 'last_name', 'phone_number']

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users.

    Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ["email", "password", "is_active", "is_superuser", 'is_staff']


class UserRoleFilter(admin.SimpleListFilter):
    """Filter users by role in Django admin.

    Allows filtering users by roles: User, Mediator, Admin.
    Attributes:
        title (str): The title of the filter.
        parameter_name (str): The name of the parameter used in the URL query.
    """

    title = 'Роль'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        """Return a list of tuples (value, display name).

        Using the list in the filtering interface.
        """
        return [
            ('USER', 'Пользователь'),
            ('MEDIATOR', 'Медиатор'),
            ('ADMIN', 'Админ'),
        ]

    def queryset(self, request, queryset):
        """
        Apply the filter to the queryset.

        Based on the selected value.
        """
        if self.value():
            return queryset.filter(role__iexact=self.value())
        return queryset


class UserAdmin(BaseUserAdmin):
    """The forms to add and change user instances."""

    form = UserChangeForm
    add_form = UserCreationForm

    def display_role(self, obj):
        """
        Display the user role in the admin user list view.

        Args:
            obj: The user object.

        Returns:
            str: The displayed user role.
        """
        role_mapping = {
            UserRoleEnum.USER.value: 'Пользователь',
            UserRoleEnum.MEDIATOR.value: 'Медиатор',
            UserRoleEnum.ADMIN.value: 'Админ',
        }
        return role_mapping.get(obj.role, obj.role)
    display_role.short_description = 'Роль'

    list_display = ["email", 'first_name',
                    'last_name', 'phone_number', 'display_role']
    list_filter = ["email", 'first_name',
                   'last_name', 'phone_number', UserRoleFilter]
    fieldsets = [
        (None, {"fields": ["email", "password", 'first_name',
         'last_name', 'phone_number', 'role']}),
        ("Permissions", {"fields": ["is_active", "is_superuser", 'is_staff']}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ['email', 'password1', 'password2', 'first_name',
                           'last_name', 'phone_number', 'is_active',
                           'is_superuser', 'is_staff'],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """
        Customize the choices for the status field to display Russian statuses.

        Args:
            db_field: The field for which to customize choices.
            request: The current request.
            **kwargs: Additional keyword arguments.

        Returns:
            The modified field with customized choices.
        """
        if db_field.name == "role":
            kwargs['choices'] = [
                ('User', 'Пользователь'),
                ('Mediator', 'Медиатор'),
                ('Admin', 'Админ')
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
