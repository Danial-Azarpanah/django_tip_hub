# Generated by Django 4.1 on 2022-09-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_user_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='کارمند'),
        ),
    ]