# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models
import location_field.models.spatial
import modelcluster.fields
import django.db.models.deletion
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ListingPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page', primary_key=True)),
                ('listing_type', bitfield.models.BitField((('venda', 'Venda'), ('locacao', 'Locação')), verbose_name='Tipos de negócio', default=None)),
                ('reference', models.CharField(blank=True, verbose_name='Referência', null=True, max_length=12)),
                ('location', location_field.models.spatial.LocationField(srid=4326, default='Point(1.0 1.0)')),
                ('bedrooms', models.PositiveIntegerField(verbose_name='Dormitórios')),
                ('suites', models.PositiveIntegerField(verbose_name='Suítes')),
                ('cars', models.PositiveIntegerField(verbose_name='Vagas de Garagem')),
                ('size_of_living_space', models.PositiveIntegerField(verbose_name='Área Construída')),
                ('size_of_land', models.PositiveIntegerField(verbose_name='Medida do Terreno')),
                ('details', wagtail.wagtailcore.fields.RichTextField(verbose_name='Detalhes')),
                ('sell_price', models.DecimalField(blank=True, verbose_name='Preço para venda', null=True, decimal_places=0, max_digits=8)),
                ('rent_price', models.DecimalField(blank=True, verbose_name='Preço para locação', null=True, decimal_places=0, max_digits=8)),
                ('amenities', models.ManyToManyField(verbose_name='Características', to='listing.Amenity')),
                ('category', models.ForeignKey(verbose_name='Categoria', to='listing.Category')),
                ('city', models.ForeignKey(verbose_name='Cidade', to='listing.City')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Neighbourhood',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('city', models.ForeignKey(to='listing.City', related_name='neighbourhood')),
            ],
        ),
        migrations.AddField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(verbose_name='Bairro', to='listing.Neighbourhood'),
        ),
        migrations.AddField(
            model_name='amenity',
            name='category',
            field=models.ForeignKey(blank=True, null=True, to='listing.Category', related_name='amenities'),
        ),
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name_plural': 'características', 'verbose_name': 'característica'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categorias', 'verbose_name': 'categoria'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cidades', 'verbose_name': 'cidade'},
        ),
        migrations.AlterModelOptions(
            name='listingpage',
            options={'verbose_name_plural': 'Imóveis', 'verbose_name': 'Imóvel'},
        ),
        migrations.AlterModelOptions(
            name='neighbourhood',
            options={'verbose_name_plural': 'bairros', 'verbose_name': 'bairro'},
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='bedrooms',
            field=models.PositiveIntegerField(blank=True, verbose_name='Dormitórios', null=True),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='cars',
            field=models.PositiveIntegerField(blank=True, verbose_name='Vagas de Garagem', null=True),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='location',
            field=location_field.models.spatial.LocationField(verbose_name='Mapa', srid=4326, default='Point(1.0 1.0)'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='rent_price',
            field=models.DecimalField(blank=True, verbose_name='Valor para locação', null=True, decimal_places=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='sell_price',
            field=models.DecimalField(blank=True, verbose_name='Valor para venda', null=True, decimal_places=0, max_digits=8),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='size_of_land',
            field=models.PositiveIntegerField(blank=True, verbose_name='Medida do Terreno', null=True),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='size_of_living_space',
            field=models.PositiveIntegerField(blank=True, verbose_name='Área Construída', null=True),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='suites',
            field=models.PositiveIntegerField(blank=True, verbose_name='Suítes', null=True),
        ),
        migrations.AlterModelOptions(
            name='amenity',
            options={'verbose_name': 'característica', 'ordering': ('name',), 'verbose_name_plural': 'características'},
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='rent_price',
            field=models.DecimalField(blank=True, verbose_name='Valor para locação', null=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='sell_price',
            field=models.DecimalField(blank=True, verbose_name='Valor para venda', null=True, decimal_places=2, max_digits=10),
        ),
        migrations.AddField(
            model_name='listingpage',
            name='address',
            field=models.CharField(blank=True, verbose_name='Endereço', help_text='Essa informação não será exibida no site', null=True, max_length=255),
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categorias', 'ordering': ('slug',), 'verbose_name': 'categoria'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'cidades', 'ordering': ('slug',), 'verbose_name': 'cidade'},
        ),
        migrations.AlterModelOptions(
            name='neighbourhood',
            options={'verbose_name_plural': 'bairros', 'ordering': ('slug',), 'verbose_name': 'bairro'},
        ),
        migrations.RemoveField(
            model_name='amenity',
            name='slug',
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(verbose_name='Bairro ou Condomínio', to='listing.Neighbourhood'),
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(blank=True, null=True, max_length=100)),
                ('image', models.ForeignKey(to='wagtailimages.Image', related_name='+')),
                ('listing', models.ForeignKey(to='listing.ListingPage', related_name='images')),
            ],
        ),
        migrations.AlterModelOptions(
            name='listingimage',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='listingimage',
            name='sort_order',
            field=models.IntegerField(blank=True, null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='listingimage',
            name='listing',
            field=modelcluster.fields.ParentalKey(to='listing.ListingPage', related_name='images'),
        ),
        migrations.RemoveField(
            model_name='listingimage',
            name='description',
        ),
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=models.ForeignKey(verbose_name='Imagem', to='wagtailimages.Image', related_name='+'),
        ),
        migrations.RemoveField(
            model_name='listingpage',
            name='amenities',
        ),
        migrations.RemoveField(
            model_name='amenity',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listingpage',
            name='category',
        ),
        migrations.AddField(
            model_name='listingpage',
            name='amenities',
            field=models.ManyToManyField(blank=True, verbose_name='Características', to='listing.Amenity'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='rent_price',
            field=models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='sell_price',
            field=models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.CreateModel(
            name='CategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page', primary_key=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterModelOptions(
            name='categorypage',
            options={'verbose_name_plural': 'categorias', 'verbose_name': 'categoria'},
        ),
        migrations.AddField(
            model_name='listingpage',
            name='maintenance_rate',
            field=models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='city',
            field=models.ForeignKey(help_text='Para adicionar mais cidades, vá até <b>Fragmentos</b> » <b>Cidades</b>', verbose_name='Cidade', to='listing.City'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='details',
            field=wagtail.wagtailcore.fields.RichTextField(verbose_name='Mais detalhes'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='listing_type',
            field=bitfield.models.BitField((('sell', 'Venda'), ('rent', 'Locação')), verbose_name='Tipos de negócio', default=None),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(help_text='Para adicionar mais bairros ou condomínios, vá até <b>Fragmentos</b> » <b>Bairros</b>', verbose_name='Bairro ou Condomínio', to='listing.Neighbourhood'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='reference',
            field=models.CharField(blank=True, verbose_name='Referência', help_text='Código de identificação do imóvel', null=True, max_length=12),
        ),
        migrations.CreateModel(
            name='Condominium',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255)),
                ('city', modelcluster.fields.ParentalKey(to='listing.City', related_name='condominiums')),
            ],
            options={
                'verbose_name_plural': 'condomínios',
                'ordering': ('slug',),
                'verbose_name': 'condomínio',
            },
        ),
        migrations.AlterField(
            model_name='neighbourhood',
            name='city',
            field=models.ForeignKey(to='listing.City', related_name='neighbourhoods'),
        ),
        migrations.AlterField(
            model_name='neighbourhood',
            name='city',
            field=modelcluster.fields.ParentalKey(to='listing.City', related_name='neighbourhoods'),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(blank=True, help_text='Para adicionar mais bairros ou condomínios, vá até <b>Fragmentos</b> » <b>Bairros</b>', null=True, verbose_name='Bairro ou Condomínio', to='listing.Neighbourhood', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AddField(
            model_name='listingpage',
            name='condominium',
            field=models.ForeignKey(blank=True, help_text='Para adicionar mais condomínios, vá até a cidade desejada em <b>Fragmentos</b> » <b>Cidades</b>', null=True, verbose_name='Condomínios', to='listing.Condominium', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='neighbourhood',
            field=models.ForeignKey(blank=True, help_text='Para adicionar mais bairros, vá até a cidade desejada em <b>Fragmentos</b> » <b>Cidades</b>', null=True, verbose_name='Bairro', to='listing.Neighbourhood', on_delete=django.db.models.deletion.SET_NULL),
        ),
        migrations.AlterField(
            model_name='listingpage',
            name='details',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Mais detalhes', null=True),
        ),
        migrations.CreateModel(
            name='ListingsPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, to='wagtailcore.Page', primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'página de imóveis',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterModelOptions(
            name='listingspage',
            options={'verbose_name': 'Imóveis'},
        ),
        migrations.AlterField(
            model_name='listingimage',
            name='image',
            field=models.ForeignKey(verbose_name='Imagem', to='dashboard.CustomImage', related_name='+'),
        ),
    ]
