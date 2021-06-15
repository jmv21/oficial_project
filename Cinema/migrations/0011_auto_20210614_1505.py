# Generated by Django 3.2 on 2021-06-14 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0010_merge_0009_auto_20210611_1256_0009_auto_20210611_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='discounts',
        ),
        migrations.AddField(
            model_name='entry',
            name='discounts',
            field=models.ManyToManyField(db_index=True, to='Cinema.Discount'),
        ),
        migrations.AddField(
            model_name='entry',
            name='reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.ImageField(blank=True, default='/movie_pics/default.jpg', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='entries',
            field=models.ManyToManyField(db_index=True, to='Cinema.Entry'),
        ),
    ]
