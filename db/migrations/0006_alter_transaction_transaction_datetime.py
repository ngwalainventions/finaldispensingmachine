# Generated by Django 5.0.2 on 2024-03-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_alter_transaction_transaction_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_datetime',
            field=models.CharField(max_length=15, null=True, verbose_name='TR time'),
        ),
    ]