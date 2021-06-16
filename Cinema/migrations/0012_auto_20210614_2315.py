# Generated by Django 3.2 on 2021-06-15 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0011_auto_20210614_1505'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'Entries'},
        ),
        migrations.AlterField(
            model_name='entry',
            name='discounts',
            field=models.ManyToManyField(blank=True, db_index=True, null=True, to='Cinema.Discount'),
        ),
    ]
