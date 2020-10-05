# Generated by Django 2.0.7 on 2018-08-15 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_auto_20180813_0541'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteAmendment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('new_tel', models.CharField(blank=True, max_length=30, null=True)),
                ('new_fax', models.CharField(blank=True, max_length=30, null=True)),
                ('new_surefax', models.CharField(blank=True, max_length=30, null=True)),
                ('new_mobile', models.CharField(blank=True, max_length=30, null=True)),
                ('new_home', models.CharField(blank=True, max_length=30, null=True)),
                ('new_priority', models.IntegerField(blank=True, default=10, null=True)),
                ('new_role', models.CharField(blank=True, max_length=100, null=True)),
                ('new_notes', models.TextField(blank=True, max_length=250, null=True)),
                ('key_contact_to_amend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.KeyContact')),
                ('person_to_amend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contacts.Person')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]