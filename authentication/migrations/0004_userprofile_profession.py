# Generated by Django 3.2.9 on 2021-11-06 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20211106_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profession',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]