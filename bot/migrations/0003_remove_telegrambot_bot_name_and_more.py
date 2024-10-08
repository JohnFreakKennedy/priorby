# Generated by Django 5.0 on 2024-06-22 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_telegrambot_group_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrambot',
            name='Bot name',
        ),
        migrations.RemoveField(
            model_name='telegrambot',
            name='Bot token',
        ),
        migrations.RemoveField(
            model_name='telegrambot',
            name='Bot username',
        ),
        migrations.RemoveField(
            model_name='telegrambot',
            name='Group ID',
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='group_id',
            field=models.CharField(default='', max_length=255, verbose_name='Group ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Bot name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='token',
            field=models.CharField(default='', max_length=255, verbose_name='Bot token'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='username',
            field=models.CharField(default='', max_length=255, verbose_name='Bot username'),
            preserve_default=False,
        ),
    ]
