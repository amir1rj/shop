# Generated by Django 4.2.4 on 2023-09-22 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_rename_couooncode_couponcode_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='couponcode',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
