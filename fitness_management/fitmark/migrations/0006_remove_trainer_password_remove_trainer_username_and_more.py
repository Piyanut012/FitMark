# Generated by Django 5.1.1 on 2024-10-09 14:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitmark', '0005_customer_email_customer_first_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='trainer',
            name='username',
        ),
        migrations.AddField(
            model_name='trainer',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='trainer',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
