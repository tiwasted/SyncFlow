# Generated by Django 5.1 on 2024-08-23 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0013_remove_b2corder_assigned_employee_and_more'),
        ('employees', '0002_employee_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2corder',
            name='assigned_employee',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_assigned_orders', to='employees.employee'),
        ),
    ]
