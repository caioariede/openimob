from django.utils.functional import cached_property
from django.db.models import Count


class ListingPageViewMixin(object):
    @cached_property
    def similar_params(self):
        params = {}
        params['category'] = self.get_parent().slug
        params['city'] = self.city.slug
        params['bedrooms'] = self.bedrooms

        if self.listing_type.sell:
            params['listing_type'] = 'sell'
            price = float(self.sell_price)

        elif self.listing_type.rent:
            params['listing_type'] = 'rent'
            price = float(self.rent_price)

        diff = float(price) * 0.20

        params['min_price'] = price - diff
        params['max_price'] = price + diff

        return params

    @cached_property
    def similar_queryset(self):
        category = self.get_parent()
        city = self.city
        listing_type = self.listing_type
        bedrooms = self.bedrooms

        qs = self.__class__.objects.child_of(category).filter(
            city=city, listing_type=listing_type,
            bedrooms__gte=bedrooms,
        )

        if listing_type.sell:
            price = float(self.sell_price)
            diff = float(price) * 0.20
            qs = qs.filter(sell_price__range=(price-diff, price+diff))

        elif listing_type.rent:
            price = float(self.rent_price)
            diff = float(price) * 0.20
            qs = qs.filter(rent_price__range=(price-diff, price+diff))

        return qs

    def get_context(self, *args, **kwargs):
        ctx = super().get_context(*args, **kwargs)
        ctx['condominiums'] = self.get_condominiums()
        ctx['neighbourhoods'] = self.get_neighbourhoods()

        return ctx

    def get_neighbourhoods(self, *args):
        qs = self.similar_queryset.filter(neighbourhood__isnull=False)

        result = []

        for row in qs.annotate(Count('neighbourhood')):
            params = self.similar_params.copy()
            params['neighbourhood'] = 'neighbourhood-{}'.format(
                row.neighbourhood.slug)

            result.append((
                row.neighbourhood,
                row.neighbourhood__count,
                params,
            ))

        if qs:
            params = self.similar_params.copy()
            params['neighbourhood'] = 'neighbourhood'

            result.insert(0, ('Todos', qs.count(), params))

        return result

    def get_condominiums(self):
        qs = self.similar_queryset.filter(condominium__isnull=False)
        result = []

        for row in qs.annotate(Count('condominium')):
            params = self.similar_params.copy()
            params['neighbourhood'] = 'condominium-{}'.format(
                row.condominium.slug)

            result.append((
                row.condominium,
                row.condominium__count,
                params,
            ))

        if qs:
            params = self.similar_params.copy()
            params['neighbourhood'] = 'condominium'

            result.insert(0, ('Todos', qs.count(), params))

        return result
