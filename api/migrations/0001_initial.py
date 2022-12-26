# Generated by Django 4.1.3 on 2022-11-18 03:11

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BeerTapDispenser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('flow_volume', models.DecimalField(decimal_places=4, max_digits=5)),
                ('status', models.CharField(choices=[('open', 'open'), ('closed', 'closed')], default='closed', editable=False, max_length=8)),
            ],
            options={
                'verbose_name': 'Beer Tap Dispenser',
                'verbose_name_plural': 'Beer Tap Dispensers',
            },
        ),
        migrations.CreateModel(
            name='BeerTapDispenserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opened_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('flow_volume', models.DecimalField(decimal_places=4, max_digits=5)),
                ('dispenser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usages', to='api.beertapdispenser')),
            ],
            options={
                'verbose_name': 'Beer Tap Dispenser History',
                'verbose_name_plural': 'Beer Tap Dispensers History',
                'ordering': ['id'],
            },
        ),
    ]
