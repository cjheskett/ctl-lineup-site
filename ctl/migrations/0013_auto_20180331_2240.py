# Generated by Django 2.0.1 on 2018-03-31 22:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0012_auto_20180302_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lineupplayer',
            name='player',
        ),
        migrations.RemoveField(
            model_name='lineup',
            name='players',
        ),
        migrations.AddField(
            model_name='lineup',
            name='set1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set1', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set2', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set3',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set3', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set4',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set4', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set5',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set5', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set6',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set6', to='ctl.Player'),
        ),
        migrations.AddField(
            model_name='lineup',
            name='set7',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='set7', to='ctl.Player'),
        ),
        migrations.AlterField(
            model_name='maps',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 31, 22, 40, 24, 72524, tzinfo=utc)),
        ),
        migrations.DeleteModel(
            name='LineupPlayer',
        ),
    ]
