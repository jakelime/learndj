# Generated by Django 3.2.16 on 2022-12-07 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_sum',
            field=models.FloatField(default=0),
        ),
    ]
