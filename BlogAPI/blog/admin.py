from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'owner', 'image', 'description',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('title', 'image', 'description')
            }
        ),
    )

    list_display = ('title', 'owner', 'posted_on', 'updated_on')
    search_fields = ('title',)
    ordering = ('-posted_on',)


admin.site.register(Post, PostAdmin)
