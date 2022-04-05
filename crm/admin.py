from cProfile import label
from concurrent.futures.process import _python_exit
import email
from django import forms
from django.contrib import admin

from crm.models import Customer, Contract, Event, Need


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]
    fieldsets = (
        ('Personal info', {'fields': (
            'last_name', 'first_name',
            'email', 'phone', 'mobile', 'company_name')}),
        ('Assignation', {'fields': (
            'sales_contact',)})
    )
    add_fieldsets = (
        ('Personal info', {'fields': ('last_name', 'first_name')}),
    )
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