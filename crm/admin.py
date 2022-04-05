from django import forms
from django.contrib import admin

from crm.models import Customer, Contract, Event, Need

class CustomerCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput)
    first_name = forms.CharField(label='First Name', widget=forms.TextInput)

    class Meta:
        model = Customer
        fields = ['last_name', 'first_name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    add_customer = CustomerCreationForm
    list_display = [field.name for field in Customer._meta.fields if field.name != "id"]
    add_fieldsets = ('last_name', 'first_name')
    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.customer_create:
            return True
        else:
            return False
    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.customer_read:
                return True
            else:
                return False
        except AttributeError: 
            return False 
    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.customer_update:
            return True
        else:
            return False
    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.customer_delete:
            return True
        else:
            return False
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contract._meta.fields if field.name != "id"]

    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.contract_create:
            return True
        else:
            return False
    
    def has_module_permission(self, request):
        try: 
            if request.user.profile_staff.contract_read:
                return True
            else:
                return False
        except AttributeError: 
            return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.contract_update:
            return True
        else:
            return False
       
    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.contract_delete:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions,


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields if field.name != "id"]

    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.event_create:
            return True
        else:
            return False
    
    def has_module_permission(self, request):
        try: 
            if request.user.profile_staff.event_read:
                return True
            else:
                return False
        except AttributeError: 
            return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.event_update:
            return True
        else:
            return False
       
    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.event_delete:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Need._meta.fields if field.name != "id"]

    filter_horizontal = ()

    def has_add_permission(self, request):
        if request.user.profile_staff.need_create:
            return True
        else:
            return False
    
    def has_module_permission(self, request):
        try: 
            if request.user.profile_staff.need_read:
                return True
            else:
                return False
        except AttributeError: 
            return False
        
    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.need_update:
            return True
        else:
            return False
       
    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.need_delete:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions