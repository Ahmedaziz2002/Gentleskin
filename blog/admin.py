from django.contrib import admin

from .models import AffiliateClick, Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at", "click_count")
    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Content", {"fields": ("title", "slug", "category", "featured_image", "excerpt", "content")}),
        ("Affiliate", {"fields": ("affiliate_link",)}),
        ("Publishing", {"fields": ("status", "created_at", "updated_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).with_related().with_click_totals()

    def click_count(self, obj):
        return obj.click_count

    click_count.short_description = "Affiliate Clicks"


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ("post", "ip_address", "session_key", "clicked_at")
    list_filter = ("post", "clicked_at")
    readonly_fields = ("post", "ip_address", "user_agent", "clicked_at")
