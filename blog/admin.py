from django.contrib import admin
from .models import Post
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ('title', 'slug', 'author', 'publish', 'status', 'pattern')
    list_filter         = ('status', 'pattern', 'created', 'publish', 'author')
    search_fields       = ('title','description1', 'description2','description3','intent')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields       = ('author',)
    date_hierarchy      = 'publish'
    ordering            = ('status', 'publish')