# Generated by Django 2.1.7 on 2019-06-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mr', '0020_surgery_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientprofile',
            name='important_notes',
            field=models.TextField(default=''),
        ),
    ]