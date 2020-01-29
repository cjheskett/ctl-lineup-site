# Generated by Django 2.0.1 on 2018-04-12 09:16

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0016_auto_20180412_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='roster',
            name='color',
            field=models.CharField(default='change me', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roster',
            name='icon_url',
            field=models.URLField(default='change me', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lineup',
            name='submit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 9, 16, 30, 463430, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maps',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 12, 9, 16, 30, 465784, tzinfo=utc)),
        ),
    ]
