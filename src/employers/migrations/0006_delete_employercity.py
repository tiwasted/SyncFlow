# Generated by Django 5.1 on 2024-08-24 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0005_employer_selected_cities_employer_selected_countries'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmployerCity',
        ),
    ]
