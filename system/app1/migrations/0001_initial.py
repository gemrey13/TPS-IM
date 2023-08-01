# Generated by Django 4.2.3 on 2023-08-01 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=20)),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DailyScrapEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ScrapItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RFID', models.CharField(max_length=100, unique=True)),
                ('weight', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('owner', 'Owner'), ('staff', 'Staff')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('scrap_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scrapitem')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.transaction')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='scraps',
            field=models.ManyToManyField(through='app1.TransactionDetail', to='app1.scrapitem'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='staff_responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scrapitem',
            name='scrap_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scraptype'),
        ),
        migrations.CreateModel(
            name='ScrapEntryDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('daily_scrap_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.dailyscrapentry')),
                ('scrap_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.scrapitem')),
            ],
        ),
        migrations.AddField(
            model_name='dailyscrapentry',
            name='scraps',
            field=models.ManyToManyField(through='app1.ScrapEntryDetail', to='app1.scrapitem'),
        ),
        migrations.AddField(
            model_name='dailyscrapentry',
            name='staff_responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
