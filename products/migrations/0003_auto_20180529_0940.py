# Generated by Django 2.0.4 on 2018-05-29 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20180529_0934'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(default='udefinert3', max_length=100),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
