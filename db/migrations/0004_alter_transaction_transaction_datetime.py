# Generated by Django 5.0.2 on 2024-03-08 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_contactusmodel_featuredpage_footercontact_footerlink_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_datetime',
            field=models.CharField(max_length=10, null=True, verbose_name='TR time'),
        ),
    ]