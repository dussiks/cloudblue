# Generated by Django 2.2.19 on 2021-06-10 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('id', 'status', 'external_id')},
        ),
    ]
