# Generated by Django 4.1.3 on 2023-09-26 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_transaction_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='balance',
        ),
    ]