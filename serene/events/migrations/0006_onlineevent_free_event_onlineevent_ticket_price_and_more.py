# Generated by Django 5.0.6 on 2024-07-06 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_eventcategory_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineevent',
            name='free_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='onlineevent',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=10),
        ),
        migrations.AddField(
            model_name='onlineevent',
            name='ticket_quantity',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='onlineevent',
            name='tickets_sold',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='venueevent',
            name='free_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='venueevent',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=10),
        ),
        migrations.AddField(
            model_name='venueevent',
            name='ticket_quantity',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AddField(
            model_name='venueevent',
            name='tickets_sold',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
