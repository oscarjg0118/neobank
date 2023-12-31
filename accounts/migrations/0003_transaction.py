# Generated by Django 4.1.3 on 2023-09-26 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_account_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, 'DEPOSIT'), (2, 'WITHDRAW')], default=1)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='accounts.account')),
            ],
        ),
    ]
