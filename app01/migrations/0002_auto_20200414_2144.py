# Generated by Django 2.0 on 2020-04-14 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_list',
            name='book_price',
            field=models.IntegerField(default=99, null=True),
        ),
    ]