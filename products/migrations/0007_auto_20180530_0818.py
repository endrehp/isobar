# Generated by Django 2.0.4 on 2018-05-30 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20180530_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='product',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='user',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
