# Generated by Django 5.1.4 on 2025-06-27 06:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0016_alter_producto_n_serie_alter_producto_nivel_minimo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='componente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.producto'),
        ),
    ]
