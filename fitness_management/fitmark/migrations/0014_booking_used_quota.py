# Generated by Django 5.1.1 on 2024-10-16 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmark', '0013_customer_free_classes_remaining_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='used_quota',
            field=models.BooleanField(default=False),
        ),
    ]
