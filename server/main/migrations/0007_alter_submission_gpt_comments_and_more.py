# Generated by Django 4.2.1 on 2023-06-16 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_publish_date_feedback_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='gpt_comments',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='gpt_mark',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
