# Generated by Django 2.0.7 on 2018-07-31 01:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0007_auto_20180724_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'get_latest_by': 'created_time', 'ordering': ['-last_mod_time'], 'verbose_name': '文章', 'verbose_name_plural': '文章列表'},
        ),
    ]