# Generated by Django 3.0.6 on 2020-05-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageprocessing', '0004_auto_20200509_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userandencodingdetail',
            name='encoding',
            field=models.TextField(verbose_name=models.FloatField()),
        ),
    ]