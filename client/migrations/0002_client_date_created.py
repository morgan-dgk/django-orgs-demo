# Generated by Django 5.0 on 2023-12-06 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
