# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listingpage',
            name='reference',
            field=models.CharField(unique=True, max_length=12, null=True, verbose_name='Referência', help_text='Código de identificação do imóvel', blank=True),
        ),
    ]
