# Generated by Django 2.0.7 on 2018-08-06 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_auto_20180806_0543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='key_contacts',
        ),
        migrations.AddField(
            model_name='keycontact',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.Organisation'),
        ),
    ]
