# Generated by Django 4.2.3 on 2023-08-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
