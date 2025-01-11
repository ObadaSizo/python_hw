# Generated by Django 5.1.4 on 2025-01-11 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsp', '0002_delete_distance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='x_coord',
            field=models.FloatField(help_text='X coordinate for visualization'),
        ),
        migrations.AlterField(
            model_name='city',
            name='y_coord',
            field=models.FloatField(help_text='Y coordinate for visualization'),
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(help_text='Distance between cities')),
                ('city1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distances_from', to='tsp.city')),
                ('city2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distances_to', to='tsp.city')),
            ],
            options={
                'verbose_name_plural': 'Distances',
                'unique_together': {('city1', 'city2')},
            },
        ),
    ]
