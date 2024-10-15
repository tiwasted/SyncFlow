# Generated by Django 5.1 on 2024-08-21 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0001_initial'),
        ('orders', '0012_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='cities',
            field=models.ManyToManyField(blank=True, related_name='employers', to='orders.city'),
        ),
        migrations.AddField(
            model_name='employer',
            name='countries',
            field=models.ManyToManyField(blank=True, related_name='employers', to='orders.country'),
        ),
    ]
