from django.contrib.gis.db import models
from django.conf import settings
from django.templatetags.l10n import localize
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django import forms

from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as trans

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, FieldRowPanel, \
    MultiFieldPanel, InlinePanel, ObjectList
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from bitfield import BitField
from location_field.models.spatial import LocationField
from input_mask.widgets import DecimalInputMask
from modelcluster.fields import ParentalKey

from .edit_handlers import ListingTabbedInterface
from .mixins import ListingPageViewMixin
from .widgets import NeighbourhoodWidget, CondominiumWidget


class CityManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


@register_snippet
class City(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    objects = CityManager()

    """
    Panels
    """
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        InlinePanel('condominiums', label='Condomínios', panels=[
            FieldRowPanel([
                FieldPanel('name', classname='col6'),
                FieldPanel('slug', classname='col6'),
            ]),
        ]),
        InlinePanel('neighbourhoods', label='Bairros', panels=[
            FieldRowPanel([
                FieldPanel('name', classname='col6'),
                FieldPanel('slug', classname='col6'),
            ]),
        ]),
    ]

    class Meta:
        ordering = ('slug',)
        verbose_name = 'cidade'
        verbose_name_plural = 'cidades'

    def __str__(self):
        return self.name


class Neighbourhood(models.Model):
    city = ParentalKey(City, related_name='neighbourhoods')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    panels = [
        FieldPanel('city'),
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    class Meta:
        ordering = ('slug',)
        verbose_name = 'bairro'
        verbose_name_plural = 'bairros'

    def __str__(self):
        return self.name


class Condominium(models.Model):
    city = ParentalKey(City, related_name='condominiums')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ('slug',)
        verbose_name = 'condomínio'
        verbose_name_plural = 'condomínios'

    def __str__(self):
        return self.name


@register_snippet
class Amenity(models.Model):
    name = models.CharField(max_length=255)

    panels = [
        FieldPanel('name'),
    ]

    class Meta:
        verbose_name = 'característica'
        verbose_name_plural = 'características'
        ordering = ('name',)

    def __str__(self):
        return self.name


class ListingsPage(Page):
    class Meta:
        verbose_name = 'Imóveis'

    """
    Settings
    """
    subpage_types = ['listing.CategoryPage']


class CategoryPage(Page):
    def get_absolute_url(self):
        return '{url}?category={slug}'.format(
            url=reverse('search'), slug=self.slug)

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    """
    Settings
    """
    subpage_types = ['listing.ListingPage']

    """
    Panels
    """
    content_panels = [
        FieldPanel('title'),
    ]


class ListingPage(ListingPageViewMixin, Page):
    listing_type = BitField(flags=settings.LISTING_TYPES,
                            verbose_name='Tipos de negócio')

    reference = models.CharField(
        max_length=12, blank=True, null=True, verbose_name='Referência',
        help_text='Código de identificação do imóvel')

    city = models.ForeignKey(
        City, verbose_name='Cidade',
        help_text=mark_safe(
            'Para adicionar mais cidades, vá até '
            '<b>Fragmentos</b> » <b>Cidades</b>'))

    neighbourhood = models.ForeignKey(
        Neighbourhood, verbose_name='Bairro',
        blank=True, null=True, on_delete=models.SET_NULL,
        help_text=mark_safe(
            'Para adicionar mais bairros, vá até a cidade desejada em '
            '<b>Fragmentos</b> » <b>Cidades</b>'))

    condominium = models.ForeignKey(
        Condominium, verbose_name='Condomínios',
        blank=True, null=True, on_delete=models.SET_NULL,
        help_text=mark_safe(
            'Para adicionar mais condomínios, vá até a cidade desejada em '
            '<b>Fragmentos</b> » <b>Cidades</b>'))

    address = models.CharField(
        max_length=255, verbose_name='Endereço', blank=True, null=True,
        help_text='Essa informação não será exibida no site')
    location = LocationField(based_fields=[
        'city', 'neighbourhood', 'address',
    ], zoom=12, default='Point(1.0 1.0)', verbose_name='Mapa')

    bedrooms = models.PositiveIntegerField(
        verbose_name='Dormitórios', blank=True, null=True)
    suites = models.PositiveIntegerField(
        verbose_name='Suítes', blank=True, null=True)
    cars = models.PositiveIntegerField(
        verbose_name='Vagas de Garagem', blank=True, null=True)

    size_of_living_space = models.PositiveIntegerField(
        verbose_name='Área Construída', blank=True, null=True)
    size_of_land = models.PositiveIntegerField(
        verbose_name='Medida do Terreno', blank=True, null=True)

    details = RichTextField(verbose_name='Mais detalhes',
                            blank=True, null=True)

    amenities = models.ManyToManyField(Amenity, verbose_name='Características',
                                       blank=True)

    sell_price = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)

    rent_price = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2)

    maintenance_rate = models.DecimalField(
        blank=True, null=True, max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

    def save(self, **kwargs):
        self.title = self.seo_title
        super().save(**kwargs)
        return self

    def get_full_amenities_list(self):
        listing_amenities = self.amenities.values_list('pk', flat=True)

        return [
            (amenity, amenity.pk in listing_amenities)
            for amenity in Amenity.objects.all()
        ]

    @cached_property
    def cover(self):
        return self.images.first()

    @property
    def sell_price_display(self):
        if not self.sell_price:
            return 'Sob consulta'
        return 'R$ {}'.format(localize(self.sell_price))

    @property
    def rent_price_display(self):
        if not self.rent_price:
            return 'Sob consulta'
        return 'R$ {}'.format(localize(self.rent_price))

    """
    Settings
    """
    subpage_types = []

    """
    Panels
    """
    location_panels = [
        FieldPanel('city', classname='full'),
        FieldPanel('neighbourhood', classname='full',
                   widget=NeighbourhoodWidget),
        FieldPanel('condominium', classname='full',
                   widget=CondominiumWidget),
        FieldPanel('address', classname='full'),
        FieldPanel('location', classname='full'),
    ]

    pricing_panels = [
        FieldPanel('listing_type', classname="full"),
        FieldPanel('sell_price', classname='full',
                   widget=DecimalInputMask(max_digits=10, decimal_places=2)),
        FieldPanel('rent_price', classname='full',
                   widget=DecimalInputMask(max_digits=10, decimal_places=2)),
        FieldPanel('maintenance_rate', classname='full',
                   widget=DecimalInputMask(max_digits=6, decimal_places=2)),
    ]

    detail_panels = [
        FieldPanel('reference', classname="full"),
        FieldPanel('bedrooms', classname='full'),
        FieldPanel('suites', classname='full'),
        FieldPanel('cars', classname='full'),
        FieldPanel('size_of_living_space', classname='full'),
        FieldPanel('size_of_land', classname='full'),
        FieldPanel('amenities', classname='full amenities',
                   widget=forms.CheckboxSelectMultiple),
        FieldPanel('details', classname='full'),
    ]

    content_panels = [
        MultiFieldPanel(location_panels, "Localização"),
        MultiFieldPanel(pricing_panels, "Valores"),
        MultiFieldPanel(detail_panels, "Detalhes"),
        InlinePanel('images', label='Imagens', panels=[
            ImageChooserPanel('image'),
        ]),
    ]

    edit_handler = ListingTabbedInterface([
        ObjectList(content_panels, heading=trans('Content')),
        ObjectList(Page.promote_panels, heading=trans('Promote')),
        ObjectList(Page.settings_panels, heading=trans('Settings'),
                   classname="settings"),
    ])


class ListingImage(Orderable, models.Model):
    listing = ParentalKey(ListingPage, related_name='images')
    image = models.ForeignKey('dashboard.CustomImage', related_name='+',
                              verbose_name='Imagem')
