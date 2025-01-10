# Generated by Django 5.1.4 on 2025-01-10 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('redirect_link', models.URLField()),
                ('token', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expiration_time', models.DurationField(blank=True, null=True)),
                ('max_uniques_clicks', models.PositiveIntegerField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Clicks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortener.links')),
            ],
        ),
    ]
