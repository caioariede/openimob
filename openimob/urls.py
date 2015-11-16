from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from dashboard import urls as dashboard_urls

from listing.views import Search
from website.views import ContactFormView


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^admin/', include(dashboard_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', Search.as_view(), name='search'),

    url(r'^ajax/neighbourhoods.json$', 'listing.views.neighbourhoods',
        name='ajax_neighbourhoods'),

    # contact form
    # TODO: move this to website.urls
    url(r'^contact/$', ContactFormView.as_view(), name='contact_form'),
    url(r'^contact/sent/$',
        TemplateView.as_view(
            template_name='contact_form/contact_form_sent.html'),
        name='contact_form_sent'),

    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
