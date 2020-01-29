# Generated by Django 2.0.1 on 2018-06-27 01:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0021_auto_20180626_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineup',
            name='submit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 27, 1, 32, 49, 207605, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maps',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 27, 1, 32, 49, 210224, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='matchreport',
            name='submit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 27, 1, 32, 49, 212798, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='resultset',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1_rs', to='ctl.Lineup'),
        ),
        migrations.AlterField(
            model_name='resultset',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2_rs', to='ctl.Lineup'),
        ),
    ]
