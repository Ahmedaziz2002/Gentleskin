from django.contrib import admin
from .models import Category, Post, AffiliateClick


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at", "click_count")  # Added click_count
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

    # Custom method to show affiliate click count
    def click_count(self, obj):
        return obj.clicks.count()  # 'clicks' is the related_name in AffiliateClick
    click_count.short_description = "Affiliate Clicks"  # Nice column header


@admin.register(AffiliateClick)
class AffiliateClickAdmin(admin.ModelAdmin):
    list_display = ("post", "ip_address", "clicked_at")
    list_filter = ("post", "clicked_at")
    readonly_fields = ("post", "ip_address", "user_agent", "clicked_at")