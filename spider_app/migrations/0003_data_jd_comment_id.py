# Generated by Django 3.2.4 on 2021-06-08 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider_app', '0002_auto_20210607_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_jd',
            name='comment_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]