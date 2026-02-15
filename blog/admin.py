from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Content", {
            "fields": ("title", "slug", "category", "featured_image", "excerpt", "content")
        }),
        ("Affiliate", {
            "fields": ("affiliate_link",)
        }),
        ("Publishing", {
            "fields": ("status", "created_at", "updated_at")
        }),
    )
