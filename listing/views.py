import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView
from django.utils.functional import cached_property
from django.db.models import Count

from .models import Neighbourhood, Condominium, ListingPage, CategoryPage


def neighbourhoods(request):
    city_slug = request.GET.get('city', None)

    listings_qs = ListingPage.objects.live().filter(city__slug=city_slug)

    # neighbourhoods
    neighbourhood_ids = listings_qs.exclude(
        neighbourhood__isnull=True
    ).order_by(
        'neighbourhood_id'
    ).distinct('neighbourhood').values_list('neighbourhood_id', flat=True)

    neighbourhoods = Neighbourhood.objects.filter(
        id__in=neighbourhood_ids,
    ).values_list('slug', 'name')

    # condominiums
    condominium_ids = listings_qs.exclude(
        condominium__isnull=True
    ).order_by(
        'condominium_id'
    ).distinct('condominium').values_list('condominium_id', flat=True)

    condominiums = Condominium.objects.filter(
        id__in=condominium_ids,
    ).values_list('slug', 'name')

    return HttpResponse(content=json.dumps({
        'neighbourhoods': list(neighbourhoods),
        'condominiums': list(condominiums),
    }), content_type='application/json')


class Search(ListView):
    model = ListingPage
    template_name = 'listing/search.html'
    context_object_name = 'listings'
    paginate_by = 30

    @cached_property
    def base_queryset(self):
        return super().get_queryset()

    @cached_property
    def filtered_queryset(self):
        return self.filter_results(self.base_queryset)

    def get(self, request, *args, **kwargs):
        reference = request.GET.get('reference')
        if reference:
            try:
                listing_page = ListingPage.objects.live().get(
                    reference=reference)
            except ListingPage.DoesNotExist:
                pass
            else:
                return HttpResponseRedirect(listing_page.url)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.filtered_queryset

        sort = self.get_sort()

        if sort == 'most_recent':
            qs = qs.order_by('-pk')
        elif sort == 'lower_price':
            qs = qs.order_by('sell_price', 'rent_price')
        elif sort == 'higher_price':
            qs = qs.order_by('-sell_price', '-rent_price')

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = self.get_categories()
        ctx['condominiums'] = self.get_condominiums()
        ctx['neighbourhoods'] = self.get_neighbourhoods()
        ctx['sort'] = self.get_sort()
        ctx['total'] = self.filtered_queryset.count()
        ctx['per_page'] = min(self.paginate_by, ctx['total'])
        ctx['price_display'] = self.get_price_display()

        return ctx

    def get_price_display(self):
        if self.request.GET.get('listing_type') == 'sell':
            return 'sell'
        return 'rent'

    def get_sort(self):
        sort = self.request.GET.get('sort')
        if sort not in ('lower_price', 'higher_price'):
            return 'most_recent'
        return sort

    def get_categories(self):
        qs = self.filter_results(self.base_queryset, exclude=('category',))
        return qs

    def get_neighbourhoods(self):
        qs = self.base_queryset.filter(neighbourhood__isnull=False)
        qs = self.filter_results(qs, exclude=('neighbourhood',))

        result = []

        for row in qs.annotate(Count('neighbourhood')):
            result.append((
                row.neighbourhood,
                row.neighbourhood__count,
                {
                    'neighbourhood': 'neighbourhood-{}'.format(
                        row.neighbourhood.slug),
                },
            ))

        if qs:
            result.insert(0, ('Todos', qs.count(), {
                'neighbourhood': 'neighbourhood',
            }))

        return result

    def get_condominiums(self):
        qs = self.base_queryset.filter(condominium__isnull=False)
        qs = self.filter_results(qs, exclude=('neighbourhood',))

        result = []

        for row in qs.annotate(Count('condominium')):
            result.append((
                row.condominium,
                row.condominium__count,
                {
                    'neighbourhood': 'condominium-{}'.format(
                        row.condominium.slug),
                },
            ))

        if qs:
            result.insert(0, ('Todos', qs.count(), {
                'neighbourhood': 'condominium',
            }))

        return result

    def filter_results(self, qs, exclude=None):
        if exclude is None:
            exclude = ()

        param = lambda key: self.request.GET.get(key)

        category = param('category')
        city = param('city')
        listing_type = param('listing_type')
        neighbourhood = param('neighbourhood')
        bedrooms = param('bedrooms')
        min_price = param('min_price')
        max_price = param('max_price')

        if listing_type == 'sell':
            is_sell = True
        elif listing_type == 'rent':
            is_sell = False
        elif listing_type:
            return qs.none()

        if category and 'category' not in exclude:
            try:
                category_page = CategoryPage.objects.get(slug=category)
            except CategoryPage.DoesNotExist:
                return qs.none()

            qs &= ListingPage.objects.child_of(category_page)

        if city:
            qs = qs.filter(city__slug=city)

        if listing_type:
            if is_sell:
                flag = ListingPage.listing_type.sell
            else:
                flag = ListingPage.listing_type.rent

            qs = qs.filter(listing_type=flag)

        if neighbourhood and 'neighbourhood' not in exclude:
            if '-' in neighbourhood:
                key, slug = neighbourhood.split('-', 1)

                if key == 'neighbourhood':
                    qs = qs.filter(neighbourhood__slug=slug)
                elif key == 'condominium':
                    qs = qs.filter(condominium__slug=slug)
                else:
                    return qs.none()

            elif neighbourhood == 'neighbourhood':
                qs = qs.filter(neighbourhood__isnull=False)

            elif neighbourhood == 'condominium':
                qs = qs.filter(condominium__isnull=False)

            else:
                return qs.none()

        if bedrooms:
            qs = qs.filter(bedrooms__gte=bedrooms)

        if min_price or max_price:
            if is_sell:
                qs = qs.filter(sell_price__range=(min_price, max_price))
            else:
                qs = qs.filter(rent_price__range=(min_price, max_price))

        return qs
