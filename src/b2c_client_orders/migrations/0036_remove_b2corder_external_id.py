# Generated by Django 5.1.1 on 2024-09-30 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0035_b2corder_updated_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b2corder',
            name='external_id',
        ),
    ]
