# Generated by Django 4.0.5 on 2022-10-27 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vaccines_control', '0002_alter_stock_last_updated_alter_stock_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockhistory',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
