# Generated by Django 2.2.7 on 2020-10-20 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_post_datatime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='datatime',
            new_name='datetime',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='datatime',
            new_name='datetime',
        ),
    ]
