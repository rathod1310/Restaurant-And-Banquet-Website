# Generated by Django 4.2.3 on 2024-02-03 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_myorder_cash_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myorder',
            name='payment_method',
            field=models.CharField(max_length=40),
        ),
    ]