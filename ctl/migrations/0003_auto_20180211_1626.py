# Generated by Django 2.0.1 on 2018-02-11 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0002_captain'),
    ]

    operations = [
        migrations.RenameField('Player', 'ctl_name', 'sc2_name'),
    ]
