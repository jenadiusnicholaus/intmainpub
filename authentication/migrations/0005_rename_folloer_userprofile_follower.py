# Generated by Django 3.2.9 on 2021-12-10 07:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20211210_1012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='folloer',
            new_name='follower',
        ),
    ]
