# Generated by Django 3.1.7 on 2021-04-29 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spotify', '0002_auto_20210429_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='artist_id',
            new_name='artist',
        ),
        migrations.RenameField(
            model_name='track',
            old_name='album_id',
            new_name='album',
        ),
    ]
