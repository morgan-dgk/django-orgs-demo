# Generated by Django 5.0 on 2023-12-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]