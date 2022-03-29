from django.contrib import admin

from crm.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields if field.name != "id"]

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