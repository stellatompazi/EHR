# Generated by Django 2.1.7 on 2019-05-13 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mr', '0009_remove_appointments_diagnosis_icd10'),
    ]

    operations = [
        migrations.CreateModel(
            name='App_icd10',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icd10_code', models.CharField(max_length=1000)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mr.Appointments')),
            ],
        ),
    ]
