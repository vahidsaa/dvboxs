# Generated by Django 5.0.4 on 2024-05-03 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_orderitem_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tayid',
            field=models.BooleanField(default=False),
        ),
    ]
