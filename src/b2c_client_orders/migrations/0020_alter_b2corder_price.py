# Generated by Django 5.1 on 2024-08-27 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0019_remove_b2corder_assigned_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2corder',
            name='price',
            field=models.DecimalField(decimal_places=0, max_digits=10),
        ),
    ]
