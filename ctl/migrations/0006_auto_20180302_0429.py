# Generated by Django 2.0.1 on 2018-03-02 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0005_auto_20180228_0414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week', models.IntegerField()),
                ('maps', models.CharField(max_length=1000)),
            ],
        ),
    ]
