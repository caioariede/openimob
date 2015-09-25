import json
from decimal import Decimal

from django.template import Library
from django.db.models import Min, Max, Avg
from django.templatetags.l10n import localize

from ..models import ListingPage, CategoryPage, City


register = Library()


@register.simple_tag
def update_querystring(request, **kwargs):
    updated = request.GET.copy()

    if '_path' in kwargs:
        path = kwargs.pop('_path')
    else:
        path = request.path

    if '_kwargs' in kwargs:
        kwargs.update(kwargs.pop('_kwargs'))

    for key, val in kwargs.items():
        updated[key] = val

    return '{path}?{qs}'.format(path=path, qs=updated.urlencode())


@register.assignment_tag
def get_listing_categories():
    return CategoryPage.objects.live().filter(numchild__gt=0)


@register.assignment_tag
def get_listing_cities():
    listings_qs = ListingPage.objects.live()

    cities_ids = listings_qs.order_by(
        'city_id'
    ).distinct('city').values_list('city_id', flat=True)

    return City.objects.filter(pk__in=cities_ids)


@register.assignment_tag
def get_random_listings(rent_num=4, sell_num=3):
    qs = ListingPage.objects.live()

    return {
        'rent': qs.filter(
            listing_type=ListingPage.listing_type.rent
        ).order_by('?')[:rent_num],
        'sell': qs.filter(
            listing_type=ListingPage.listing_type.sell
        ).order_by('?')[:sell_num],
    }


@register.simple_tag
def print_listing_min_max_prices_json():
    qs = ListingPage.objects.live()

    rent_prices = qs.filter(
        rent_price__gt=0
    ).aggregate(min=Min('rent_price'), max=Max('rent_price'))

    sell_prices = qs.filter(
        sell_price__gt=0
    ).aggregate(min=Min('sell_price'), max=Max('sell_price'),
                avg=Avg('sell_price'))

    rent_min = max(rent_prices['min'] or 0, 500)
    rent_max = max(rent_prices['max'] or 0, rent_min)

    rent_choices = []
    if rent_max > 0:
        rent_diff = rent_min
        rent_choices.append(rent_min)
        while rent_min < rent_max:
            rent_min += rent_diff
            rent_choices.append(min(rent_min, rent_max))

    sell_min = sell_prices['min'] or 0
    sell_max = sell_prices['max'] or 0
    sell_avg = sell_prices['avg'] or 0

    sell_choices_aux = [
        Decimal('5000.00'), Decimal('10000.00'), Decimal('50000.00'),
        Decimal('100000.00'), Decimal('200000.00'), Decimal('300000.00'),
        Decimal('400000.00'), Decimal('500000.00'), Decimal('1000000.00'),
        Decimal('3000000.00'), Decimal('5000000.00'), Decimal('10000000.00'),
        Decimal('100000000.00'),
    ]

    last_choice = None
    sell_choices = []

    for i, choice in enumerate(sell_choices_aux):
        if choice > sell_min and last_choice and not sell_choices:
            sell_choices.append(last_choice)
        elif sell_max > choice > sell_avg:
            sell_choices.append(choice)
        elif choice > sell_max:
            sell_choices.append(choice)
            break

        last_choice = choice

    dct = {
        'rent': [(float(v), 'R$ ' + localize(v)) for v in rent_choices],
        'sell': [(float(v), 'R$ ' + localize(v)) for v in sell_choices],
    }

    return json.dumps(dct)
