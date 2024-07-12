# Generated by Django 5.0.7 on 2024-07-12 09:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
        ('orders', '0003_remove_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='assigned_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_orders', to='employees.employee'),
        ),
    ]
