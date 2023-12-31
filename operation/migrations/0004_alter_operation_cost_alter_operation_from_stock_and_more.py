# Generated by Django 5.0 on 2023-12-08 17:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_operation_cost_operation_price_operation_quantity'),
        ('product', '0003_product_creator_product_last_editor'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='cost',
            field=models.FloatField(blank=True, null=True, verbose_name='Стоимость'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='from_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='from_stocks', to='stock.stock', verbose_name='Исходный склад'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product', verbose_name='Ресурс'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='quantity',
            field=models.FloatField(blank=True, null=True, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stocks', to='stock.stock', verbose_name='Склад'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='to_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='to_stocks', to='stock.stock', verbose_name='Новый склад'),
        ),
        migrations.AlterField(
            model_name='operation',
            name='type',
            field=models.CharField(choices=[('admission', 'Поступление'), ('departure', 'Продажа'), ('transfer', 'Передача'), ('recalc', 'Переучет')], max_length=1024, verbose_name='Операция'),
        ),
    ]
