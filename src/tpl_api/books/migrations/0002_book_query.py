# Generated by Django 4.0.2 on 2022-02-21 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='query',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
