from django.db.models import Q
from django.contrib import admin
from datetime import datetime

from authentication.models import User
from crm.models import Customer, Contract, Event, Need

date_now = datetime.now()


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_filter = [['sales_contact', admin.RelatedOnlyFieldListFilter]]
    list_display = [field.name for field in Customer._meta.fields]
    fieldsets = (
        ('Personal info', {'fields': (
            'last_name', 'first_name',
            'email', 'phone', 'mobile', 'company_name')}),
        ('Assignation', {'fields': (
            'sales_contact',)})
    )

    def has_add_permission(self, request, obj=None):
        user_perms = request.user.profile_staff
        if user_perms.customer_CRUD_all or user_perms.customer_CRU_assigned:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            user_perms = request.user.profile_staff
            if (user_perms.customer_read) or (
                user_perms.customer_CRU_assigned) or (
                    user_perms.customer_CRUD_all):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_module_permission(self, request, obj=None):
        try:
            user_perms = request.user.profile_staff
            if (user_perms.customer_read) or (
                user_perms.customer_CRU_assigned) or (
                    user_perms.customer_CRUD_all):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.profile_staff.customer_CRUD_all:
            return True
        elif request.user.profile_staff.customer_CRU_assigned:
            if request.user == obj.sales_contact:
                return True
            else:
                return False
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.customer_CRUD_all:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomerAdmin, self).get_form(request, obj, **kwargs)
        list_sales_user = User.objects.filter(profile_staff__id=2)
        if form.base_fields:
            form.base_fields['sales_contact'].queryset = list_sales_user
        if request.user.profile_staff.customer_CRU_assigned and (
            not request.user.profile_staff.customer_CRUD_all
        ):
            list_sales_user = User.objects.filter(id=request.user.id)
            if form.base_fields:
                form.base_fields['sales_contact'].queryset = list_sales_user
                
        return form


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Contract._meta.fields
        ]
    fieldsets = (
        (None, {'fields': (
            'title',
            'date_start_contract',
            'date_end_contract',
            'signed',
            'customer_assigned',)}),
    )

    def has_add_permission(self, request):
        user_perms = request.user.profile_staff
        if user_perms.contract_CRU_assigned or (
            user_perms.contract_CRUD_all
        ):
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            user_perms = request.user.profile_staff
            if user_perms.contract_read or (
                user_perms.contract_CRU_assigned) or (
                    user_perms.contract_CRUD_all
                    ):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            user_perms = request.user.profile_staff
            if user_perms.contract_read or (
                user_perms.contract_CRU_assigned) or (
                    user_perms.contract_CRUD_all
                    ):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        if request.user.profile_staff.contract_CRUD_all:
            return True
        elif request.user.profile_staff.contract_CRU_assigned:
            if request.user == obj.customer_assigned.sales_contact:
                return True
            else:
                return False
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.contract_CRUD_all:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContractAdmin, self).get_form(request, obj, **kwargs)
        if request.user.profile_staff.contract_CRUD_all:
            customer_list = Customer.objects.all()
            form.base_fields['customer_assigned'].queryset = customer_list
        elif request.user.profile_staff.contract_CRU_assigned:
            customer_list = Customer.objects.filter(sales_contact=request.user)
            if form.base_fields:
                form.base_fields['customer_assigned'].queryset = customer_list
        return form


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Event._meta.fields]

    fieldsets = (
        ("Event Details", {'fields': (
            'title',
            'date_started',
            'date_finished',)}),
        ("Staff Contact Support", {'fields': (
            'support_contact',)}),
        ("Contract Signed and Assigned", {'fields': (
            'contract_assigned',)}),
    )

    def has_add_permission(self, request):
        user_perms = request.user.profile_staff
        if user_perms.name == "SUPPORT":
            return False
        elif user_perms.event_CRU_assigned or user_perms.event_CRUD_all:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            user_perms = request.user.profile_staff
            if user_perms.event_read or (
                user_perms.event_CRU_assigned
            ) or user_perms.event_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            user_perms = request.user.profile_staff
            if user_perms.event_read or (
                user_perms.event_CRU_assigned
            ) or user_perms.event_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        user_perms = request.user.profile_staff
        if user_perms.event_CRUD_all:
            return True
        elif user_perms.event_CRU_assigned:
            if obj.contract_assigned.customer_assigned.sales_contact == (
               request.user):
                return True
            else:
                return False
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.profile_staff.event_CRUD_all:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, obj, **kwargs)
        if request.user.profile_staff.event_CRUD_all:
            contract_list = Contract.objects.filter(Q(signed=True) & Q(
                date_end_contract__gt=datetime.now()))
            if form.base_fields:
                form.base_fields['contract_assigned'].queryset = contract_list
            return form
        elif request.user.profile_staff.event_CRU_assigned:
            if request.user.profile_staff.id == 3:
                if form.base_fields:
                    form.base_fields[
                        'contract_assigned'].widget.attrs[
                            'disabled'] = 'disabled'
                if form.base_fields:
                    form.base_fields[
                        'support_contact'].widget.attrs[
                            'disabled'] = 'disabled'
            customer_list = Customer.objects.filter(
                sales_contact=request.user)
            contract_list = Contract.objects.filter(
                Q(customer_assigned__in=customer_list) & Q(signed=True) & Q(
                    date_end_contract__gt=datetime.now()))
            if form.base_fields:
                form.base_fields['contract_assigned'].queryset = contract_list
        return form


@admin.register(Need)
class NeedAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Need._meta.fields]

    fieldsets = (
        ("Need Details", {'fields': (
            'title',)}),
        ("Finished ?", {'fields': (
            'success',)}),
        ("Event assigned", {'fields': (
            'event_assigned',)}),
    )

    def has_add_permission(self, request):
        user_perms = request.user.profile_staff
        if user_perms.need_CRU_assigned or user_perms.need_CRUD_all:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            user_perms = request.user.profile_staff
            if user_perms.need_read or (
               user_perms.need_CRU_assigned) or (user_perms.need_CRUD_all):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            user_perms = request.user.profile_staff
            if user_perms.need_read or (
               user_perms.need_CRU_assigned) or (user_perms.need_CRUD_all):
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return False
        if obj.event_assigned.date_finished.isoformat() < date_now.isoformat():
            return False
        user_perms = request.user.profile_staff
        if user_perms.need_CRUD_all:
            return True
        elif user_perms.need_CRU_assigned:
            if obj.event_assigned.support_contact == (
               request.user):
                return True
            else:
                return False
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return False
        if obj.event_assigned.date_finished.isoformat() < date_now.isoformat():
            return False
        if request.user.profile_staff.need_CRUD_all:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_form(self, request, obj=None, **kwargs):
        form = super(NeedAdmin, self).get_form(request, obj, **kwargs)
        if request.user.profile_staff.need_CRU_assigned:
            event_list = Event.objects.filter(Q(
                support_contact=request.user) & Q(
                    date_finished__gt=datetime.now()))
            if form.base_fields:
                form.base_fields['event_assigned'].queryset = event_list
        if request.user.profile_staff.need_CRUD_all:
            event_list = Event.objects.filter(date_finished__gt=datetime.now())
            if form.base_fields:
                form.base_fields['event_assigned'].queryset = event_list
        return form
