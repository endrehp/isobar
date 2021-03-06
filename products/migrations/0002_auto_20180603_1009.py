# Generated by Django 2.0.4 on 2018-06-03 10:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 9, 32, 943341, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 9, 32, 942301, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 3, 10, 9, 32, 941315, tzinfo=utc)),
        ),
    ]
