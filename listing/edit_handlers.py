from wagtail.wagtailadmin.edit_handlers import TabbedInterface
from wagtail.wagtailcore import hooks

from input_mask.fields import DecimalField


def get_form_class(BaseListingForm):
    class ListingForm(BaseListingForm):
        sell_price = DecimalField(required=False, label='Valor para venda')
        rent_price = DecimalField(required=False, label='Valor para locação')
        maintenance_rate = DecimalField(
            required=False, label='Valor do condomínio')

        def __setattr__(self, name, value):
            if name == 'save_m2m' and not self.instance.pk:
                value = lambda: None
            return super(ListingForm, self).__setattr__(name, value)

    return ListingForm


class ListingTabbedInterface(TabbedInterface):
    def bind_to_model(self, model):
        cls = super().bind_to_model(model)
        base_form_class = cls.get_form_class(model)
        cls._form_class = get_form_class(base_form_class)
        return cls


@hooks.register('after_create_page')
def save_amenities(request, page):
    from listing.models import Amenity

    amenities_ids = request.POST.getlist('amenities')
    amenities = Amenity.objects.filter(pk__in=amenities_ids)

    for amenity in amenities:
        page.amenities.add(amenity)
