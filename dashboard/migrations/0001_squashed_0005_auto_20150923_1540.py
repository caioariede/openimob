# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailimages.models
import wagtail.wagtailadmin.taggable
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wagtailimages', '0008_image_created_at_index'),
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(blank=True, null=True, verbose_name='Title', max_length=255)),
                ('file', models.ImageField(width_field='width', height_field='height', verbose_name='File', upload_to=wagtail.wagtailimages.models.get_upload_to)),
                ('width', models.IntegerField(editable=False, verbose_name='Width')),
                ('height', models.IntegerField(editable=False, verbose_name='Height')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created at')),
                ('focal_point_x', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_y', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_width', models.PositiveIntegerField(null=True, blank=True)),
                ('focal_point_height', models.PositiveIntegerField(null=True, blank=True)),
                ('file_size', models.PositiveIntegerField(editable=False, null=True)),
                ('tags', taggit.managers.TaggableManager(help_text=None, to='taggit.Tag', verbose_name='Tags', through='taggit.TaggedItem', blank=True)),
                ('uploaded_by_user', models.ForeignKey(editable=False, verbose_name='Uploaded by user', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, wagtail.wagtailadmin.taggable.TagSearchable),
        ),
        migrations.CreateModel(
            name='CustomRendition',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('file', models.ImageField(width_field='width', height_field='height', upload_to='images')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('focal_point_key', models.CharField(editable=False, max_length=255, blank=True, default='')),
                ('filter', models.ForeignKey(to='wagtailimages.Filter', related_name='+')),
                ('image', models.ForeignKey(to='dashboard.CustomImage', related_name='renditions')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together=set([('image', 'filter', 'focal_point_key')]),
        ),
        migrations.AddField(
            model_name='customimage',
            name='brightness',
            field=models.IntegerField(default=0),
        ),
    ]
