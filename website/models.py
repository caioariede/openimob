from wagtail.wagtailcore.models import Page


class HomePage(Page):
    class Meta:
        verbose_name = 'Página Inicial'

    subpage_types = ['website.DummyPage', 'listing.ListingsPage']


class DummyPage(Page):
    class Meta:
        verbose_name = 'Página genérica'
