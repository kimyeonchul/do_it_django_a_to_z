from django.contrib import admin
from .models import Post, Category, Tag

admin.site.register(Post)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Tag,TagAdmin)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)