# Generated by Django 3.1.4 on 2020-12-11 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tab', '0002_auto_20201211_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='transactions_id',
        ),
        migrations.AlterField(
            model_name='transactions',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
