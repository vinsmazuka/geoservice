# Generated by Django 4.0.1 on 2022-02-13 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showmap', '0002_alter_city_foundation_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='population',
            field=models.CharField(max_length=100),
        ),
    ]
