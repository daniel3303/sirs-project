# Generated by Django 2.1.4 on 2018-12-06 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_auto_20181206_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='content',
            field=models.BinaryField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='key',
            field=models.BinaryField(default=b'H8k_Xp2ItIAXvn-1L-Gb5sAFqAsM_L5f7KL6x_x53dU=', max_length=32),
        ),
        migrations.AlterField(
            model_name='file',
            name='mac',
            field=models.BinaryField(max_length=64),
        ),
    ]
