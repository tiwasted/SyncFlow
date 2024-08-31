# Generated by Django 5.1 on 2024-08-31 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2b_client_orders', '0019_remove_b2border_assigned_employee_and_more'),
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
        migrations.AlterField(
            model_name='b2border',
            name='status',
            field=models.CharField(choices=[('in_processing', 'В обработке'), ('in_waiting', 'В ожидании'), ('completed', 'Выполнен'), ('cancelled', 'Отменен')], default='in_processing', max_length=20),
        ),
    ]
