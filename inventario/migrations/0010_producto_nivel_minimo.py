# Generated by Django 5.1.4 on 2025-06-25 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_movimiento_responsable'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='nivel_minimo',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
