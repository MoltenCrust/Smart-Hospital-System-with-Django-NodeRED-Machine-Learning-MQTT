# Generated by Django 4.2.6 on 2023-11-11 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHospitalSystem', '0003_alter_actuator_list_activation_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actuator_list',
            name='turn_on_when_exceeded',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='historicalactuator_list',
            name='turn_on_when_exceeded',
            field=models.BooleanField(default=True),
        ),
    ]
