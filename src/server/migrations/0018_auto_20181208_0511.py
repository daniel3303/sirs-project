# Generated by Django 2.1.4 on 2018-12-08 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_auto_20181207_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='key',
            field=models.BinaryField(default=None, max_length=32),
        ),
        migrations.AddField(
            model_name='user',
            name='mac',
            field=models.BinaryField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='role',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='editors', to='server.File'),
        ),
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='server.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
    ]
