# Generated by Django 2.0.4 on 2018-05-29 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='images/profile_default.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='poeng',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='profile',
            name='saldo',
            field=models.IntegerField(default=0),
        ),
    ]
