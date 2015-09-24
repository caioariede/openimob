# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields
import location_field.models.spatial
import bitfield.models
import wagtail.wagtailcore.fields
import listing.mixins


class Migration(migrations.Migration):

    dependencies = [
        # ('dashboard', '0001_initial'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'característica',
                'verbose_name_plural': 'características',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
            options={
                'verbose_name': 'cidade',
                'verbose_name_plural': 'cidades',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('city', modelcluster.fields.ParentalKey(related_name='condominiums', to='listing.City')),
            ],
            options={
                'verbose_name': 'condomínio',
                'verbose_name_plural': 'condomínios',
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sort_order', models.IntegerField(blank=True, null=True, editable=False)),
                ('image', models.ForeignKey(verbose_name='Imagem', to='dashboard.CustomImage', related_name='+')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ListingPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True)),
                ('listing_type', bitfield.models.BitField((('sell', 'Venda'), ('rent', 'Locação')), default=None, verbose_name='Tipos de negócio')),
                ('reference', models.CharField(null=True, blank=True, verbose_name='Referência', help_text='Código de identificação do imóvel', max_length=12)),
                ('address', models.CharField(null=True, blank=True, verbose_name='Endereço', help_text='Essa informação não será exibida no site', max_length=255)),
                ('location', location_field.models.spatial.LocationField(default='Point(1.0 1.0)', verbose_name='Mapa', srid=4326)),
                ('bedrooms', models.PositiveIntegerField(blank=True, verbose_name='Dormitórios', null=True)),
                ('suites', models.PositiveIntegerField(blank=True, verbose_name='Suítes', null=True)),
                ('cars', models.PositiveIntegerField(blank=True, verbose_name='Vagas de Garagem', null=True)),
                ('size_of_living_space', models.PositiveIntegerField(blank=True, verbose_name='Área Construída', null=True)),
                ('size_of_land', models.PositiveIntegerField(blank=True, verbose_name='Medida do Terreno', null=True)),
                ('details', wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Mais detalhes', null=True)),
                ('sell_price', models.DecimalField(max_digits=10, blank=True, decimal_places=2, null=True)),
                ('rent_price', models.DecimalField(max_digits=10, blank=True, decimal_places=2, null=True)),
                ('maintenance_rate', models.DecimalField(max_digits=6, blank=True, decimal_places=2, null=True)),
                ('amenities', models.ManyToManyField(blank=True, verbose_name='Características', to='listing.Amenity')),
                ('city', models.ForeignKey(verbose_name='Cidade', help_text='Para adicionar mais cidades, vá até <b>Fragmentos</b> » <b>Cidades</b>', to='listing.City')),
                ('condominium', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Condomínios', help_text='Para adicionar mais condomínios, vá até a cidade desejada em <b>Fragmentos</b> » <b>Cidades</b>', to='listing.Condominium', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Imóvel',
                'verbose_name_plural': 'Imóveis',
            },
            bases=(listing.mixins.ListingPageViewMixin, 'wagtailcore.page'),
        ),
        migrations.CreateModel(
            name='ListingsPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, to='wagtailcore.Page', auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Imóveis',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('city', modelcluster.fields.ParentalKey(related_name='neighbourhoods', to='listing.City')),
            ],
            options={
                'verbose_name': 'bairro',
                'verbose_name_plural': 'bairros',
                'ordering': ('slug',),
            },
        ),
        migrations.AddField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='Bairro', help_text='Para adicionar mais bairros, vá até a cidade desejada em <b>Fragmentos</b> » <b>Cidades</b>', to='listing.Neighbourhood', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listingimage',
            name='listing',
            field=modelcluster.fields.ParentalKey(related_name='images', to='listing.ListingPage'),
        ),
    ]
