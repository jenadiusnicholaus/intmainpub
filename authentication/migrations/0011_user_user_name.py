# Generated by Django 3.2.9 on 2021-11-13 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]
