# Generated by Django 5.1 on 2024-08-31 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('b2c_client_orders', '0024_alter_b2corder_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='b2corder',
            name='status',
            field=models.CharField(choices=[('in_processing', 'В обработке'), ('in_waiting', 'В ожидании'), ('completed', 'Выполнен'), ('cancelled', 'Отменен')], default='in_processing', max_length=20),
        ),
    ]
