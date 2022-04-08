from django.db.models import Q
from django.contrib import admin
from authentication.models import User

from crm.models import Customer, Contract, Event, Need


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
        if request.user.profile_staff.customer_CRU_assigned:
            return True
        elif request.user.profile_staff.customer_CRUD_all:
            return True
        else:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.profile_staff.customer_CRU_assigned:
                return True
            elif request.user.profile_staff.customer_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_module_permission(self, request, obj=None):
        try:
            if request.user.profile_staff.customer_CRU_assigned:
                return True
            elif request.user.profile_staff.customer_CRUD_all:
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
        if request.user.profile_staff.customer_CRUD_all:
            list_sales_user = User.objects.filter(profile_staff__id=2)
            form.base_fields['sales_contact'].queryset = list_sales_user
            return form
        elif request.user.profile_staff.customer_CRU_assigned:
            list_sales_user = User.objects.filter(id=request.user.id)
            if form.base_fields:
                form.base_fields['sales_contact'].queryset = list_sales_user
            return form
        else:
            return None


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
        if request.user.profile_staff.contract_CRU_assigned:
            return True
        elif request.user.profile_staff.contract_CRUD_all:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.contract_CRU_assigned:
                return True
            elif request.user.profile_staff.contract_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.profile_staff.contract_CRU_assigned:
                return True
            elif request.user.profile_staff.contract_CRUD_all:
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
            print(obj.customer_assigned.sales_contact)
            print("email", request.user.email)
            if request.user == obj.customer_assigned.sales_contact:
                return True
            else:
                return None
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
            return form
        elif request.user.profile_staff.contract_CRU_assigned:
            customer_list = Customer.objects.filter(sales_contact=request.user)
            if form.base_fields:
                form.base_fields['customer_assigned'].queryset = customer_list
                return form
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
        if request.user.profile_staff.event_CRU_assigned:
            return True
        elif request.user.profile_staff.event_CRUD_all:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.event_CRU_assigned:
                return True
            elif request.user.profile_staff.event_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.profile_staff.event_CRU_assigned:
                return True
            elif request.user.profile_staff.event_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.event_CRU_assigned:
            return True
        elif request.user.profile_staff.event_CRUD_all:
            return True
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
        if request.user.profile_staff.event_CRUD_all:
            form = super(EventAdmin, self).get_form(request, obj, **kwargs)
            contract_list = Contract.objects.filter(signed=True)
            form.base_fields['contract_assigned'].queryset = contract_list
            return form
        elif request.user.profile_staff.event_CRU_assigned:
            form = super(EventAdmin, self).get_form(request, obj, **kwargs)
            customer_list = Customer.objects.filter(
                sales_contact=request.user)
            contract_list = Contract.objects.filter(
                Q(customer_assigned__in=customer_list) | Q(signed=True))
            form.base_fields['contract_assigned'].queryset = contract_list
            return form
        else:
            return None


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
        if request.user.profile_staff.need_CRU_assigned:
            return True
        elif request.user.profile_staff.need_CRUD_all:
            return True
        else:
            return False

    def has_module_permission(self, request):
        try:
            if request.user.profile_staff.need_CRU_assigned:
                return True
            elif request.user.profile_staff.need_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_view_permission(self, request, obj=None):
        try:
            if request.user.profile_staff.need_CRU_assigned:
                return True
            elif request.user.profile_staff.need_CRUD_all:
                return True
            else:
                return False
        except AttributeError:
            return False

    def has_change_permission(self, request, obj=None):
        if request.user.profile_staff.need_CRU_assigned:
            return True
        elif request.user.profile_staff.need_CRUD_all:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
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
        if request.user.profile_staff.need_CRUD_all:
            form = super(NeedAdmin, self).get_form(request, obj, **kwargs)
            event_list = Event.objects.all()
            form.base_fields['event_assigned'].queryset = event_list
            return form
        elif request.user.profile_staff.need_CRU_assigned:
            form = super(NeedAdmin, self).get_form(request, obj, **kwargs)
            event_list = Event.objects.filter(
                support_contact=request.user)
            form.base_fields['event_assigned'].queryset = event_list
            return form
        else:
            return None
