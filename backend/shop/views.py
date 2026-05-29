from urllib.parse import quote

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _

from .models import Category, Product


def home(request):
    featured_products = Product.objects.filter(is_active=True)[:8]
    categories_qs = Category.objects.all()
    context = {
        "featured_products": featured_products,
        "categories": categories_qs,
    }
    return render(request, "shop/home.html", context)


def catalog(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.filter(is_active=True).select_related("category")

    if query:
        products = products.filter(title__icontains=query)

    context = {
        "products": products,
        "query": query,
    }
    return render(request, "shop/catalog.html", context)


def categories(request):
    categories_qs = Category.objects.all()
    return render(request, "shop/categories.html", {"categories": categories_qs})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(is_active=True)
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "shop/category_detail.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("gallery"),
        slug=slug,
        is_active=True,
    )
    absolute_url = request.build_absolute_uri(product.get_absolute_url())
    whatsapp_message = _(
        "Здравствуйте!\n"
        "Хочу заказать товар: {title}\n\n"
        "Цена: {price}\n\n"
        "Ссылка: {url}"
    ).format(title=product.title, price=product.price, url=absolute_url)
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={quote(str(whatsapp_message))}"

    context = {
        "product": product,
        "whatsapp_url": whatsapp_url,
    }
    return render(request, "shop/product_detail.html", context)


def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html", {"whatsapp_phone": settings.WHATSAPP_PHONE})


def custom_404(request, exception):
    return render(request, "shop/404.html", status=404)
