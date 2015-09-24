from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel


class ContentPage(Page):
    body = RichTextField()

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname='full'),
    ]
