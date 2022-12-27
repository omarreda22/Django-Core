from django.contrib import admin

from .models import Car, Driver


class CustomCarAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__email', 'name', 'user__id']
    raw_id_fields = ['user']  # will change dropdown for user id
    readonly_fields = ['updated_by']

    class Meta:
        model = Car

    def save_model(self, request, obj, form, change):
        """
            updated_by will select by updated user
        """
        if change:
            obj.updated_by = request.user

        # if create new one
        # else:
        #     obj.updated_by = request.user
        obj.save()


admin.site.register(Car, CustomCarAdmin)
admin.site.register(Driver)
