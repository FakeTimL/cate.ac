# Generated by Django 4.2.1 on 2023-06-09 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_question_mark_minimum'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Topic',
            new_name='Chapter',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='topics',
            new_name='chapters',
        ),
    ]
