# Generated by Django 5.1.1 on 2024-10-08 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmark', '0004_remove_customer_email_remove_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
