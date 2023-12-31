# Generated by Django 4.1 on 2023-04-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Model", "0010_alter_seat_qr_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="reservation_hours",
            field=models.IntegerField(
                choices=[(1, "1小时"), (2, "2小时"), (3, "3小时"), (4, "4小时")],
                default=4,
                verbose_name="预约时长",
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="have_charge",
            field=models.PositiveIntegerField(default=0, verbose_name="是否有充电设备"),
        ),
    ]
