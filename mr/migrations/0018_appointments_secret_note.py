# Generated by Django 2.1.7 on 2019-06-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mr', '0017_favourites'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='secret_note',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
