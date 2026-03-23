from django.contrib import admin
from .models import Post, Category, Location


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Location)
