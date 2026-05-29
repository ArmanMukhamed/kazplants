from django.conf import settings
from django.db.models import Case, IntegerField, Value, When

from .models import Category


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


def site_settings(request):
    profile = settings.STORE_PROFILE
    return {
        "site_name": profile["name"],
        "site_positioning": profile["positioning"],
        "site_description": profile["description"],
        "site_whatsapp_phone": profile["whatsapp_phone"],
        "site_instagram_url": profile["instagram_url"],
        "site_contact_phone": profile["phone"],
        "site_contact_address": profile["address"],
        "site_city": profile["city"],
        "site_hours": profile["hours"],
        "footer_categories": ordered_categories()[:6],
    }
