import json

from django.http import HttpResponse
from django.template.defaultfilters import slugify

from listing.models import Neighbourhood, Condominium


def neighbourhoods(request):
    city_id = request.GET.get('city', None)
    term = slugify(request.GET.get('term', ''))

    results = Neighbourhood.objects.filter(
        city__id=city_id,
        slug__contains=term,
    ).values_list('id', 'name')

    results = [{'id': r[0], 'text': r[1]} for r in results]

    return HttpResponse(content=json.dumps(results),
                        content_type='application/json')


def condominiums(request):
    city_id = request.GET.get('city', None)
    term = slugify(request.GET.get('term', ''))

    results = Condominium.objects.filter(
        city__id=city_id,
        slug__contains=term,
    ).values_list('id', 'name')

    results = [{'id': r[0], 'text': r[1]} for r in results]

    return HttpResponse(content=json.dumps(results),
                        content_type='application/json')
