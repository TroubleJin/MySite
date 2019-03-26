# Generated by Django 2.1.7 on 2019-03-26 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book_list',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=64, null=True)),
                ('book_description', models.CharField(max_length=64, null=True)),
                ('book_country', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='publisher_list',
            fields=[
                ('publisher_id', models.AutoField(primary_key=True, serialize=False)),
                ('publisher_name', models.CharField(max_length=64, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='book_list',
            name='book_publish',
            field=models.ForeignKey(on_delete='CASCADE', to='app01.publisher_list'),
        ),
    ]
