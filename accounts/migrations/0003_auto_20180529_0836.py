# Generated by Django 2.0.4 on 2018-05-29 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180529_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/images/profile_default.png', upload_to='images/'),
        ),
    ]
