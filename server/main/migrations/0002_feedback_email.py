# Generated by Django 4.2.1 on 2023-06-14 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='email',
            field=models.TextField(blank=True),
        ),
    ]
