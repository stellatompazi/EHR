# Generated by Django 2.1.7 on 2019-06-12 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userMessages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='was_read',
            field=models.BooleanField(default=False),
        ),
    ]
