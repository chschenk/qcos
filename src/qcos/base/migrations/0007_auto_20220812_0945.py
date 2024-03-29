# Generated by Django 3.2 on 2022-08-12 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20220812_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='picture_rights',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registration',
            name='rules_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registration',
            name='staff_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
