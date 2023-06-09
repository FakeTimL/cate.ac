# Generated by Django 4.2.1 on 2023-06-09 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_topic_parent_topic_resources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='main.topic'),
        ),
    ]