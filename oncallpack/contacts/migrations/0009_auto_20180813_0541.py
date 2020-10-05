# Generated by Django 2.0.7 on 2018-08-13 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0008_auto_20180807_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keycontact',
            name='notes',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='keycontact',
            name='tfh',
            field=models.BooleanField(default=False, verbose_name='24hr'),
        ),
    ]
