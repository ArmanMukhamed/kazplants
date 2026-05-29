import csv
import io
import os
import zipfile
from decimal import Decimal, InvalidOperation

from django import forms
from django.contrib import admin, messages
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.text import slugify

from .models import Category, Product, ProductImage


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(label="CSV файл")


class BulkImageUploadForm(forms.Form):
    images_zip = forms.FileField(label="ZIP с изображениями")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image_preview", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 30

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    change_list_template = "admin/shop/product_changelist.html"

    list_display = (
        "title",
        "sku",
        "brand",
        "category",
        "price",
        "stock_status",
        "is_popular",
        "is_new",
        "is_active",
        "image_preview",
        "created_at",
    )
    list_filter = ("category", "stock_status", "is_popular", "is_new", "is_active", "care_level", "brand", "created_at")
    search_fields = ("title", "sku", "slug", "description", "characteristics", "origin_country", "brand")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("price", "stock_status", "is_popular", "is_new", "is_active")
    inlines = [ProductImageInline]
    list_select_related = ("category",)
    list_per_page = 40
    save_on_top = True

    fieldsets = (
        ("Основное", {"fields": ("title", "slug", "sku", "brand", "pot_size", "category", "price", "is_active", "is_popular", "is_new")}),
        (
            "Параметры растения",
            {"fields": ("stock_status", "height", "diameter", "origin_country", "care_level", "light_requirements", "watering")},
        ),
        ("Контент", {"fields": ("description", "characteristics", "image")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-csv/", self.admin_site.admin_view(self.import_csv_view), name="shop_product_import_csv"),
            path("bulk-images/", self.admin_site.admin_view(self.bulk_images_view), name="shop_product_bulk_images"),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["import_csv_url"] = reverse("admin:shop_product_import_csv")
        extra_context["bulk_images_url"] = reverse("admin:shop_product_bulk_images")
        return super().changelist_view(request, extra_context=extra_context)

    def import_csv_view(self, request):
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = form.cleaned_data["csv_file"]
                if not csv_file.name.endswith(".csv"):
                    self.message_user(request, "Загрузите CSV файл.", level=messages.ERROR)
                    return HttpResponseRedirect(request.path)

                decoded = csv_file.read().decode("utf-8-sig")
                reader = csv.DictReader(io.StringIO(decoded))
                created_count = 0
                updated_count = 0

                for row in reader:
                    title = (row.get("title") or "").strip()
                    if not title:
                        continue

                    slug = (row.get("slug") or "").strip() or slugify(title)
                    sku = (row.get("sku") or "").strip()
                    brand = (row.get("brand") or "").strip()
                    pot_size = (row.get("pot_size") or "").strip()
                    category_name = (row.get("category") or "Без категории").strip()

                    category, _ = Category.objects.get_or_create(
                        name=category_name,
                        defaults={"slug": slugify(category_name) or "kategoriya"},
                    )

                    stock_status = (row.get("stock_status") or Product.StockStatus.IN_STOCK).strip()
                    if stock_status not in dict(Product.StockStatus.choices):
                        stock_status = Product.StockStatus.IN_STOCK

                    care_level = (row.get("care_level") or "").strip()
                    if care_level and care_level not in dict(Product.CareLevel.choices):
                        care_level = ""

                    def parse_decimal(value):
                        value = (value or "").strip().replace(",", ".")
                        if not value:
                            return None
                        try:
                            return Decimal(value)
                        except (InvalidOperation, ValueError):
                            return None

                    defaults = {
                        "title": title,
                        "slug": slug,
                        "sku": sku,
                        "brand": brand,
                        "pot_size": pot_size,
                        "category": category,
                        "description": (row.get("description") or "").strip(),
                        "price": parse_decimal(row.get("price")) or Decimal("0"),
                        "stock_status": stock_status,
                        "height": parse_decimal(row.get("height")),
                        "diameter": parse_decimal(row.get("diameter")),
                        "origin_country": (row.get("origin_country") or "").strip(),
                        "care_level": care_level,
                        "light_requirements": (row.get("light_requirements") or "").strip(),
                        "watering": (row.get("watering") or "").strip(),
                        "characteristics": (row.get("characteristics") or "").strip(),
                        "is_active": str(row.get("is_active", "1")).strip().lower() in {"1", "true", "yes", "y", "да"},
                        "is_popular": str(row.get("is_popular", "0")).strip().lower() in {"1", "true", "yes", "y", "да"},
                        "is_new": str(row.get("is_new", "0")).strip().lower() in {"1", "true", "yes", "y", "да"},
                        "meta_title": (row.get("meta_title") or "").strip(),
                        "meta_description": (row.get("meta_description") or "").strip(),
                    }

                    if sku:
                        product, created = Product.objects.update_or_create(sku=sku, defaults=defaults)
                    else:
                        product, created = Product.objects.update_or_create(slug=slug, defaults=defaults)

                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                self.message_user(request, f"CSV импорт завершен. Создано: {created_count}, обновлено: {updated_count}", level=messages.SUCCESS)
                return HttpResponseRedirect(reverse("admin:shop_product_changelist"))
        else:
            form = CSVImportForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Импорт товаров из CSV",
            "form": form,
        }
        return TemplateResponse(request, "admin/shop/csv_import.html", context)

    def bulk_images_view(self, request):
        if request.method == "POST":
            form = BulkImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                zip_file = form.cleaned_data["images_zip"]
                if not zip_file.name.endswith(".zip"):
                    self.message_user(request, "Загрузите ZIP архив.", level=messages.ERROR)
                    return HttpResponseRedirect(request.path)

                attached = 0
                skipped = 0
                with zipfile.ZipFile(zip_file) as archive:
                    for file_name in archive.namelist():
                        if file_name.endswith("/"):
                            continue

                        base_name = os.path.basename(file_name)
                        stem, ext = os.path.splitext(base_name)
                        if ext.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                            continue

                        product = Product.objects.filter(sku=stem).first() or Product.objects.filter(slug=stem).first()
                        if not product:
                            skipped += 1
                            continue

                        file_content = archive.read(file_name)
                        product.image.save(base_name, ContentFile(file_content), save=True)
                        attached += 1

                self.message_user(request, f"Загрузка завершена. Обновлено изображений: {attached}, пропущено: {skipped}", level=messages.SUCCESS)
                return HttpResponseRedirect(reverse("admin:shop_product_changelist"))
        else:
            form = BulkImageUploadForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "title": "Массовая загрузка изображений",
            "form": form,
        }
        return TemplateResponse(request, "admin/shop/bulk_images.html", context)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image_preview")
    search_fields = ("product__title",)
    list_per_page = 50

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"

    image_preview.short_description = "Preview"
