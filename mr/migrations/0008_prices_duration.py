# Generated by Django 2.1.7 on 2019-05-02 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mr', '0007_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='prices',
            name='duration',
            field=models.IntegerField(default=15, validators=[django.core.validators.MaxValueValidator(300), django.core.validators.MinValueValidator(1)]),
        ),
    ]
