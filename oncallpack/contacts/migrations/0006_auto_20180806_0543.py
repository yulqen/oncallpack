# Generated by Django 2.0.7 on 2018-08-06 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0005_auto_20180805_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='iata_code',
            field=models.CharField(blank=True, max_length=3, null=True, verbose_name='IATA code'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='icao_code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='ICAO code'),
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='key_contacts',
        ),
        migrations.AddField(
            model_name='organisation',
            name='key_contacts',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='key_contacts_org', to='contacts.KeyContact'),
        ),
    ]
