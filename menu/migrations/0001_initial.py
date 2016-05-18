# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200, blank=True, unique=True)),
                ('lvl', models.IntegerField(editable=False, default=0)),
                ('menu', models.ForeignKey(related_name='all_items', to='menu.Menu', blank=True, null=True)),
                ('parent', models.ForeignKey(to='menu.MenuItem', blank=True, null=True)),
                ('root', models.ForeignKey(related_name='all_children', to='menu.MenuItem', blank=True, null=True)),
            ],
        ),
    ]
