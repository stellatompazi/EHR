# Generated by Django 2.1.7 on 2019-05-13 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mr', '0008_prices_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointments',
            name='diagnosis_icd10',
        ),
    ]
