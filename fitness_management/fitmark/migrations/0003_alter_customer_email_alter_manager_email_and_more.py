# Generated by Django 5.1.1 on 2024-09-21 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmark', '0002_alter_class_name_alter_customer_password_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='email',
            field=models.EmailField(max_length=50, unique=True),
        ),
    ]
