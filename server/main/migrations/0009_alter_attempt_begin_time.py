# Generated by Django 4.2.1 on 2023-06-16 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_attempt_sheet_alter_submission_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='begin_time',
            field=models.DateTimeField(),
        ),
    ]
