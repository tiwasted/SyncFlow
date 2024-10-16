# Generated by Django 5.0.7 on 2024-07-11 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='employer',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='employers.employer'),
            preserve_default=False,
        ),
    ]
