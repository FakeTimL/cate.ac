# Generated by Django 4.2.1 on 2023-06-16 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_submission_delete_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]