# Generated by Django 3.2.9 on 2021-11-12 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20211111_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topics',
            old_name='id',
            new_name='uuid',
        ),
    ]
