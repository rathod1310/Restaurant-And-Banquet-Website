# Generated by Django 4.2.3 on 2024-02-03 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_alter_myorder_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myorder',
            name='date',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]