# Generated by Django 5.1.4 on 2024-12-17 23:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_alter_post_created_at_alter_post_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 18, 0, 55, 2, 987068)),
        ),
    ]