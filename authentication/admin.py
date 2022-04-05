from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from authentication.models import User as MyUser
from authentication.models import ProfileStaff


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'last_name', 'first_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'last_name', 'first_name')


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'last_name', 'first_name', 'profile_staff')
    list_filter = ('profile_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name')}),
        ('Permissions', {'fields': ('profile_staff',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ("User Login", {'fields': ('email', 'password', 'password2')}),
        ('Personal info', {'fields': ('last_name', 'first_name')}),
        ('Permissions', {'fields': ('profile_staff',)}),
    )
    search_fields = ('email', 'profile_staff')
    ordering = ('last_name', 'email', 'profile_staff')
    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.manage_staff_user_crud:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)


@admin.register(ProfileStaff)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in ProfileStaff._meta.fields if field.name != "id"
        ]

    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            False

    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.manage_staff_user_crud:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            False

    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.manage_staff_user_crud:
            return True
        else:
            False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
