from django.conf.urls import url

from dashboard.views import neighbourhoods, condominiums


urlpatterns = [
    url(r'^ajax/neighbourhoods.json', neighbourhoods,
        name='dashboard_neighbourhoods_json'),
    url(r'^ajax/condominiums.json', condominiums,
        name='dashboard_condominiums_json'),
]
