# Generated by Django 5.1 on 2024-08-31 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2b_client_orders', '0020_alter_b2border_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b2border',
            name='employee_name',
        ),
        migrations.RemoveField(
            model_name='b2border',
            name='employee_phone',
        ),
        migrations.AddField(
            model_name='b2border',
            name='scheduled_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
