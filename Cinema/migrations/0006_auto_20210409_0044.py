# Generated by Django 3.2 on 2021-04-09 04:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0005_auto_20210408_2351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projection',
            old_name='partner points cost',
            new_name='monetary_cost',
        ),
        migrations.RemoveField(
            model_name='projection',
            name='monetary cost',
        ),
        migrations.AddField(
            model_name='projection',
            name='partner_points_cost',
            field=models.DecimalField(decimal_places=2, default=20, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
