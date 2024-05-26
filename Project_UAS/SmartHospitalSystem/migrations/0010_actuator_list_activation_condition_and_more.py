# Generated by Django 4.2.7 on 2023-11-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartHospitalSystem', '0009_remove_actuator_list_activation_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actuator_list',
            name='activation_condition',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='actuator_list',
            name='threshold',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactuator_list',
            name='activation_condition',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='historicalactuator_list',
            name='threshold',
            field=models.FloatField(blank=True, null=True),
        ),
    ]