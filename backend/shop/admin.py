from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image_preview", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "stock_status",
        "is_popular",
        "is_new",
        "is_active",
        "image_preview",
        "created_at",
    )
    list_filter = ("category", "stock_status", "is_popular", "is_new", "is_active", "care_level", "created_at")
    search_fields = ("title", "slug", "description", "characteristics", "origin_country")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "stock_status", "is_popular", "is_new", "is_active")
    inlines = [ProductImageInline]

    fieldsets = (
        ("Основное", {"fields": ("title", "slug", "category", "price", "is_active", "is_popular", "is_new")}),
        (
            "Параметры растения",
            {"fields": ("stock_status", "height", "diameter", "origin_country", "care_level", "light_requirements", "watering")},
        ),
        ("Контент", {"fields": ("description", "characteristics", "image")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_preview")
    search_fields = ("product__title",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"
