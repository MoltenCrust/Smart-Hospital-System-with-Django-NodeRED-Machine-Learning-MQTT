# Generated by Django 4.2.6 on 2023-11-11 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHospitalSystem', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsensor_list_int',
            name='max',
        ),
        migrations.RemoveField(
            model_name='historicalsensor_list_int',
            name='min',
        ),
        migrations.RemoveField(
            model_name='historicalsensor_list_int',
            name='step',
        ),
        migrations.RemoveField(
            model_name='sensor_list_int',
            name='max',
        ),
        migrations.RemoveField(
            model_name='sensor_list_int',
            name='min',
        ),
        migrations.RemoveField(
            model_name='sensor_list_int',
            name='step',
        ),
    ]
