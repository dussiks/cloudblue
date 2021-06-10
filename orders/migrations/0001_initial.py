# Generated by Django 2.2.19 on 2021-06-10 15:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('new', 'New'), ('accepted', 'Accepted'), ('failed', 'Failed')], default='new', max_length=12, verbose_name='Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('external_id', models.CharField(max_length=128, verbose_name='External identifier')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Amount')),
                ('price', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Price')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='orders.Order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='details', to='orders.Product')),
            ],
        ),
    ]