# Generated by Django 5.1 on 2024-08-26 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2b_client_orders', '0016_remove_b2border_assigned_employee_and_more'),
        ('employees', '0002_employee_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b2border',
            name='assigned_employee',
        ),
        migrations.AddField(
            model_name='b2border',
            name='assigned_employee',
            field=models.ManyToManyField(blank=True, related_name='%(class)s_assigned_orders', to='employees.employee'),
        ),
    ]
