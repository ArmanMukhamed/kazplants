from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponseRedirect
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from shop.sitemaps import CategorySitemap, ProductSitemap

sitemaps = {
    "products": ProductSitemap,
    "categories": CategorySitemap,
}


def legacy_language_prefix_redirect(request, path=""):
    target = f"/{path}"
    if not target.startswith("/"):
        target = f"/{target}"
    if target == "//":
        target = "/"
    query_string = request.META.get("QUERY_STRING")
    if query_string:
        target = f"{target}?{query_string}"
    return HttpResponseRedirect(target)


urlpatterns = [
    re_path(r"^(?:kk|en)/(?P<path>.*)$", legacy_language_prefix_redirect),
    path("", include("shop.urls")),
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("favicon.ico", RedirectView.as_view(url=f"{settings.STATIC_URL}img/favicon.svg", permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "shop.views.custom_404"
handler500 = "shop.views.custom_500"
