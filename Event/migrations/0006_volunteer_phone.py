# Generated by Django 4.2 on 2023-11-27 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Event', '0005_attendee_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='phone',
            field=models.CharField(default=771773440, max_length=255),
            preserve_default=False,
        ),
    ]
