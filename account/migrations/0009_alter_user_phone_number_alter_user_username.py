# Generated by Django 4.1 on 2022-08-20 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_user_phone_number_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True, verbose_name='نام کاربری'),
        ),
    ]