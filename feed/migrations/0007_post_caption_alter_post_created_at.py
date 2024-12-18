# Generated by Django 5.1.4 on 2024-12-18 01:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0006_alter_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
