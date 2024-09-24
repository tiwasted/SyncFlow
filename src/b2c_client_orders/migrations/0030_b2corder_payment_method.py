# Generated by Django 5.1 on 2024-09-15 06:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0029_remove_b2corder_scheduled_date'),
        ('orders', '0013_paymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='b2corder',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.paymentmethod'),
        ),
    ]
