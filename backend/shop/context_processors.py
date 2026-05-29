from django.conf import settings

from .models import Category


def site_settings(request):
    return {
        "site_whatsapp_phone": settings.WHATSAPP_PHONE,
        "site_instagram_url": "https://instagram.com/kazplants",
        "site_contact_city": "Астана, Казахстан",
        "site_contact_phone": "+7 775 756 00 46",
        "footer_categories": Category.objects.all()[:6],
    }
