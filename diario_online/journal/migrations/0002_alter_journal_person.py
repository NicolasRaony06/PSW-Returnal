# Generated by Django 5.1.4 on 2025-01-08 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='person',
            field=models.ManyToManyField(blank=True, null=True, to='journal.person'),
        ),
    ]
