# Generated by Django 4.1 on 2023-04-10 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Model", "0006_alter_room_number_of_seats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="room_id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="自习室ID"
            ),
        ),
        migrations.AlterField(
            model_name="seat",
            name="seat_id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="座位ID"
            ),
        ),
    ]
