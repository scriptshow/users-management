# Generated by Django 2.1.5 on 2019-09-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='iban',
            field=models.CharField(max_length=34, unique=True),
        ),
    ]