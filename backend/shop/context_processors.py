from django.conf import settings

from .models import Category


def site_settings(request):
    profile = settings.STORE_PROFILE
    return {
        "site_name": profile["name"],
        "site_whatsapp_phone": profile["whatsapp_phone"],
        "site_instagram_url": profile["instagram_url"],
        "site_contact_phone": profile["phone"],
        "site_contact_city": profile["address"],
        "footer_categories": Category.objects.all()[:6],
    }
