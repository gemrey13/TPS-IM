# Generated by Django 4.2.3 on 2023-08-02 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_scrapitem_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapitem',
            name='RFID',
            field=models.CharField(blank=True, default='sample', max_length=100),
        ),
        migrations.AlterField(
            model_name='scrapitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
