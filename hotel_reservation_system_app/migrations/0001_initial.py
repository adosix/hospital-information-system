# Generated by Django 3.1.1 on 2020-09-06 23:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomNumber', models.SlugField(max_length=255, unique=True)),
                ('sleeps', models.TextField()),
                ('price', models.TextField()),
            ],
            options={
                'ordering': ['roomNumber'],
            },
        ),
    ]