# Generated by Django 4.2.1 on 2023-06-17 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_rename_author_sheet_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='user_answer',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
