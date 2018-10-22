# Generated by Django 2.0.4 on 2018-06-03 10:54

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180603_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='n_ratings',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 54, 3, 41460, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 54, 3, 40787, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 54, 3, 40223, tzinfo=utc)),
        ),
    ]