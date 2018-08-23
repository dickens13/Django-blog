# Generated by Django 2.0.7 on 2018-08-02 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mod', '0015_remove_poll_ip_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=40, verbose_name='昵称')),
                ('content', models.TextField(max_length=400, verbose_name='评论内容')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b', to='mod.Article')),
                ('reply', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='r', to='mod.Comments')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
            },
        ),
    ]