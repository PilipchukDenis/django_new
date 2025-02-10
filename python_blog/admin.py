from django.contrib import admin
from .models import Category, Post, Tag


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    readonly_fields = ["slug"]


class PostAdmin(admin.ModelAdmin):
    search_fields = ["title", "content"]
    # Поля, которые будут отображаться в списке постов
    list_display = ["title", "created_at", "updated_at", "category"]
    # Сделаем так, чтобы slug отображался, но нельзя было его редактировать
    readonly_fields = ["slug"]

class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "slug"]
    readonly_fields = ["slug"]

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)