# Generated by Django 4.2.4 on 2023-09-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_couooncode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couooncode',
            name='type',
            field=models.CharField(choices=[('percent', 'percent'), ('value', 'value')], max_length=7),
        ),
    ]
