# Generated by Django 4.2.4 on 2023-08-18 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('randcode', models.SmallIntegerField()),
                ('expiresion_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
