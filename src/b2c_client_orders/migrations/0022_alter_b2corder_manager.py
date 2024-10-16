# Generated by Django 5.1 on 2024-08-29 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0021_b2corder_manager'),
        ('employers', '0011_managercityassignment_is_primary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2corder',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b2c_orders', to='employers.manager'),
        ),
    ]
