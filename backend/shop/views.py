from urllib.parse import quote

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Case, IntegerField, Q, Value, When
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def ordered_categories():
    order_map = {
        "derevya-i-sazhency": 1,
        "komnatnye-rasteniya": 2,
        "cvety": 3,
        "derevya-i-kustarniki": 4,
        "kashpo-i-aksessuary": 5,
        "gotovye-resheniya": 6,
    }
    whens = [When(slug=slug, then=Value(pos)) for slug, pos in order_map.items()]
    return Category.objects.annotate(
        order_rank=Case(*whens, default=Value(100), output_field=IntegerField())
    ).order_by("order_rank", "name")


def home(request):
    categories_qs = ordered_categories()
    popular_products = Product.objects.filter(is_active=True, is_popular=True).select_related("category")[:8]
    new_products = Product.objects.filter(is_active=True, is_new=True).select_related("category")[:8]

    if not popular_products:
        popular_products = Product.objects.filter(is_active=True).select_related("category")[:8]
    if not new_products:
        new_products = Product.objects.filter(is_active=True).select_related("category").order_by("-created_at")[:8]

    context = {
        "popular_products": popular_products,
        "new_products": new_products,
        "categories": categories_qs,
        "hero_whatsapp_url": f"https://wa.me/{settings.WHATSAPP_PHONE}",
    }
    return render(request, "shop/home.html", context)


def catalog(request):
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "default").strip() or "default"
    stock = request.GET.get("stock", "").strip()

    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    min_height = request.GET.get("min_height", "").strip()
    max_height = request.GET.get("max_height", "").strip()
    min_diameter = request.GET.get("min_diameter", "").strip()
    max_diameter = request.GET.get("max_diameter", "").strip()

    products = Product.objects.filter(is_active=True).select_related("category")
    categories_qs = ordered_categories()

    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(characteristics__icontains=query)
            | Q(sku__icontains=query)
            | Q(brand__icontains=query)
        )

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if stock:
        products = products.filter(stock_status=stock)

    def apply_decimal_range(qs, field_name, min_value, max_value):
        if min_value:
            try:
                qs = qs.filter(**{f"{field_name}__gte": float(min_value)})
            except ValueError:
                pass
        if max_value:
            try:
                qs = qs.filter(**{f"{field_name}__lte": float(max_value)})
            except ValueError:
                pass
        return qs

    products = apply_decimal_range(products, "price", min_price, max_price)
    products = apply_decimal_range(products, "height", min_height, max_height)
    products = apply_decimal_range(products, "diameter", min_diameter, max_diameter)

    sort_map = {
        "default": "-created_at",
        "price_asc": "price",
        "price_desc": "-price",
        "title_asc": "title",
    }
    products = products.order_by(sort_map.get(sort, "-created_at"))

    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "products": page_obj.object_list,
        "categories": categories_qs,
        "query": query,
        "selected_category": selected_category,
        "sort": sort,
        "stock": stock,
        "min_price": min_price,
        "max_price": max_price,
        "min_height": min_height,
        "max_height": max_height,
        "min_diameter": min_diameter,
        "max_diameter": max_diameter,
        "stock_choices": Product.StockStatus.choices,
    }
    return render(request, "shop/catalog.html", context)


def categories(request):
    categories_qs = ordered_categories()
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

    whatsapp_message = (
        "Здравствуйте!\n"
        "Хочу заказать товар: {title}\n"
        "Цена: {price}\n"
        "Высота: {height}\n"
        "Диаметр: {diameter}\n"
        "Ссылка: {url}"
    ).format(
        title=product.title,
        price=product.price,
        height=f"{product.height} см" if product.height else "-",
        diameter=f"{product.diameter} см" if product.diameter else "-",
        url=absolute_url,
    )
    whatsapp_url = f"https://wa.me/{settings.WHATSAPP_PHONE}?text={quote(str(whatsapp_message))}"

    similar_products = (
        Product.objects.filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)
        .select_related("category")[:4]
    )

    context = {
        "product": product,
        "whatsapp_url": whatsapp_url,
        "similar_products": similar_products,
    }
    return render(request, "shop/product_detail.html", context)


def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html")


def health(request):
    return HttpResponse("OK", content_type="text/plain")


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def custom_404(request, exception):
    return render(request, "shop/404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)
