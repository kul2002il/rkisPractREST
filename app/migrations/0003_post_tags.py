# Generated by Django 2.2.7 on 2020-10-19 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201019_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='app.Tag'),
        ),
    ]
