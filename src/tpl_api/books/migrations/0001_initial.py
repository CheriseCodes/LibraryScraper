# Generated by Django 4.0.2 on 2022-02-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=300)),
                ('contributors', models.CharField(blank=True, default='', max_length=200)),
                ('branches', models.TextField()),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
