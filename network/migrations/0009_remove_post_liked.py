# Generated by Django 4.2.4 on 2023-11-23 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_remove_post_likes_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='liked',
        ),
    ]
