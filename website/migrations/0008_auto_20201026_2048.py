# Generated by Django 3.1 on 2020-10-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20201026_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='kode',
            field=models.CharField(default='E27745002FB1', max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='properti',
            name='kode',
            field=models.CharField(default='355801E64CB5', max_length=16, unique=True),
        ),
    ]
