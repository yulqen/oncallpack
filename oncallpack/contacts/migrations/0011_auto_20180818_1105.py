# Generated by Django 2.0.7 on 2018-08-18 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0010_remoteamendment'),
    ]

    operations = [
        migrations.AddField(
            model_name='keycontact',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='remoteamendment',
            name='key_contact_to_amend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.KeyContact'),
        ),
        migrations.AlterField(
            model_name='remoteamendment',
            name='person_to_amend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.Person'),
        ),
    ]
