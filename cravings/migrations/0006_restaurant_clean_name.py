# Generated by Django 3.1.1 on 2021-02-02 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cravings', '0005_auto_20210126_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='clean_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
