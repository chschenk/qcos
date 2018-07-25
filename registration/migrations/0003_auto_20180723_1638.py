# Generated by Django 2.0.7 on 2018-07-23 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_registration_camp'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='comment',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registration',
            name='paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]