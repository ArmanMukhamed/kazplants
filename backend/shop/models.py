from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category_detail", kwargs={"slug": self.slug})


class Product(models.Model):
    class StockStatus(models.TextChoices):
        IN_STOCK = "in_stock", _("В наличии")
        PREORDER = "preorder", _("Под заказ")
        OUT_OF_STOCK = "out_of_stock", _("Нет в наличии")

    class CareLevel(models.TextChoices):
        EASY = "easy", _("Легкий")
        MEDIUM = "medium", _("Средний")
        HARD = "hard", _("Требовательный")

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    stock_status = models.CharField(max_length=20, choices=StockStatus.choices, default=StockStatus.IN_STOCK)
    height = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True, help_text=_("Высота в см"))
    diameter = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True, help_text=_("Диаметр в см"))
    origin_country = models.CharField(max_length=100, blank=True)
    care_level = models.CharField(max_length=20, choices=CareLevel.choices, blank=True)
    light_requirements = models.CharField(max_length=150, blank=True)
    watering = models.CharField(max_length=150, blank=True)
    characteristics = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=320, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("shop:product_detail", kwargs={"slug": self.slug})


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="products/gallery/")

    class Meta:
        verbose_name = _("Доп. изображение товара")
        verbose_name_plural = _("Доп. изображения товара")

    def __str__(self):
        return f"{self.product.title} image #{self.pk}"
