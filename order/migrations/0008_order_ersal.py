# Generated by Django 5.0.4 on 2024-05-04 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_bayane_alter_order_tayid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ersal',
            field=models.BooleanField(default=False, verbose_name='ارسال شده'),
        ),
    ]
