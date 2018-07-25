# Generated by Django 2.0.7 on 2018-07-23 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camps', '0002_auto_20180718_1325'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='camp',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='camps.Camp'),
            preserve_default=False,
        ),
    ]
