# Generated by Django 4.2.1 on 2023-05-31 12:25

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_to_be_verified', models.EmailField(blank=True, max_length=254)),
                ('email_verification_token', models.BinaryField(blank=True, max_length=128)),
                ('avatar', models.ImageField(blank=True, upload_to=accounts.models.user_directory_path)),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
