from django import forms
from django.core.urlresolvers import reverse_lazy

from django_select2 import widgets


class AjaxCitySelect(widgets.Select2Widget):
    def init_options(self):
        super().init_options()
        self.options['theme'] = 'wagtail'

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['data-filter-by'] = '[name=city]'
        attrs['data-filter-url'] = self.filter_url
        return super().render(name, value, attrs)


class NeighbourhoodWidget(AjaxCitySelect):
    filter_url = reverse_lazy('dashboard_neighbourhoods_json')

    @property
    def media(self):
        return forms.Media()


class CondominiumWidget(AjaxCitySelect):
    filter_url = reverse_lazy('dashboard_condominiums_json')

    @property
    def media(self):
        return forms.Media()
