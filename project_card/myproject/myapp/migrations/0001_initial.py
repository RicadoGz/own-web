# Generated by Django 5.0.6 on 2024-06-23 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suite', models.IntegerField(choices=[(0, 'SPADE'), (1, 'HEART'), (2, 'CLUB'), (3, 'DIAMOND')])),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.IntegerField(default=0)),
                ('cards', models.ManyToManyField(to='myapp.card')),
            ],
        ),
    ]
