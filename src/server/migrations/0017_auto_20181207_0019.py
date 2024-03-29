# Generated by Django 2.1.4 on 2018-12-07 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0016_auto_20181206_0448'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='mac',
            field=models.BinaryField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.BinaryField(default=None),
        ),
        migrations.AlterField(
            model_name='file',
            name='key',
            field=models.BinaryField(default=None, max_length=32),
        ),
        migrations.AlterField(
            model_name='file',
            name='mac',
            field=models.BinaryField(default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name='role',
            name='file',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='editors', to='server.File'),
        ),
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='server.User'),
        ),
    ]
