# Generated by Django 4.1 on 2022-08-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=0, max_length=11, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='user', max_length=50, verbose_name='نام کاربری'),
        ),
    ]
