# Generated by Django 5.1.2 on 2024-10-30 05:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_app', '0002_user_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OilType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oil_type', models.CharField(choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric')], max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarForSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('model_year', models.IntegerField()),
                ('km_driven', models.IntegerField()),
                ('accidental_background', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mileage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('front_image', models.ImageField(blank=True, null=True, upload_to='car_images/front/')),
                ('leftside_img', models.ImageField(blank=True, null=True, upload_to='car_images/leftside/')),
                ('rightside_img', models.ImageField(blank=True, null=True, upload_to='car_images/rightside/')),
                ('back_image', models.ImageField(blank=True, null=True, upload_to='car_images/back/')),
                ('registration_number', models.CharField(max_length=20, unique=True)),
                ('insurance_end_date', models.DateField()),
                ('ownership_type', models.CharField(choices=[('1st', '1st Owner'), ('2nd', '2nd Owner'), ('3rd', '3rd Owner'), ('4th+', '4th or more Owners')], max_length=4)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('created_time', models.TimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_app.brand')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_app.user')),
                ('oil_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_app.oiltype')),
            ],
        ),
    ]
