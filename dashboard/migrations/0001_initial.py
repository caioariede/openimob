# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
from django.conf import settings
import wagtail.wagtailadmin.taggable
import wagtail.wagtailimages.models


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailimages', '0008_image_created_at_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True, blank=True, verbose_name='Title')),
                ('file', models.ImageField(height_field='height', upload_to=wagtail.wagtailimages.models.get_upload_to, verbose_name='File', width_field='width')),
                ('width', models.IntegerField(verbose_name='Width', editable=False)),
                ('height', models.IntegerField(verbose_name='Height', editable=False)),
                ('created_at', models.DateTimeField(db_index=True, verbose_name='Created at', auto_now_add=True)),
                ('focal_point_x', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_y', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_width', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_height', models.PositiveIntegerField(null=True, blank=True)),
                ('file_size', models.PositiveIntegerField(null=True, editable=False)),
                ('brightness', models.IntegerField(default=0)),
                ('tags', taggit.managers.TaggableManager(blank=True, to='taggit.Tag', through='taggit.TaggedItem', help_text=None, verbose_name='Tags')),
                ('uploaded_by_user', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL, editable=False, verbose_name='Uploaded by user')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('file', models.ImageField(height_field='height', upload_to='images', width_field='width')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(max_length=255, blank=True, default='', editable=False)),
                ('filter', models.ForeignKey(to='wagtailimages.Filter', related_name='+')),
                ('image', models.ForeignKey(to='dashboard.CustomImage', related_name='renditions')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
    ]
