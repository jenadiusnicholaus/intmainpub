# Generated by Django 3.2.9 on 2021-11-13 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_rename_user_name_user_usename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='usename',
            new_name='username',
        ),
    ]
