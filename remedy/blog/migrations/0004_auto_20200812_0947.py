# Generated by Django 3.0.8 on 2020-08-12 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200811_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='dislike',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='answer',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
