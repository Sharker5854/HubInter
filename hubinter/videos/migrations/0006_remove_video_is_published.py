# Generated by Django 3.2.2 on 2021-08-12 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20210730_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='is_published',
        ),
    ]