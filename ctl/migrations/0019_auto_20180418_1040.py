# Generated by Django 2.0.1 on 2018-04-18 10:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ctl', '0018_auto_20180412_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submit_time', models.DateTimeField(default=datetime.datetime(2018, 4, 18, 10, 40, 47, 750890, tzinfo=utc))),
                ('comments', models.CharField(max_length=100000)),
                ('set1result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set2result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set3result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set4result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set5result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set6result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set71result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set72result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set73result', models.CharField(choices=[('win', 'Win'), ('loss', 'Loss'), ('admin', 'Admin'), ('na', 'N/A')], max_length=10)),
                ('set71map', models.CharField(max_length=100)),
                ('set72map', models.CharField(max_length=100)),
                ('set73map', models.CharField(max_length=100)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctl.Roster')),
            ],
        ),
        migrations.AlterField(
            model_name='lineup',
            name='submit_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 18, 10, 40, 47, 748396, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='maps',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 4, 18, 10, 40, 47, 749593, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='matchreport',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctl.Maps'),
        ),
    ]
