# Generated by Django 2.0.7 on 2018-07-24 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0006_auto_20180724_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chicategory',
            name='first_type',
        ),
        migrations.RemoveField(
            model_name='article',
            name='chicategory',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mod.Category', verbose_name='所属分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=models.ImageField(blank=True, upload_to='images', verbose_name='图片'),
        ),
        migrations.DeleteModel(
            name='ChiCategory',
        ),
    ]
