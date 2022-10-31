from django.contrib import admin
from .models import Blog


class BlogAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'slug',
        'descrip',
        'state',
        'view_count',
        'publish_date',
        'active',
        'get_age'
    ]
    readonly_fields = ['get_age']
    list_display = ['title', 'active']
    list_filter = ['active']
    list_editable = ['active']
    search_fields = ['title']
    list_per_page = 3
    ordering = ['-active']

    def get_age(self, obj, *args, **kwargs):
        return str(obj.age)

    class Meta:
        model = Blog


admin.site.register(Blog, BlogAdmin)
