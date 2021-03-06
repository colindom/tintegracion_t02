# Generated by Django 3.1.7 on 2021-04-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='genre',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='track',
            name='name',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='track',
            name='times_played',
            field=models.IntegerField(default=0),
        ),
    ]
