# Generated by Django 4.1 on 2022-08-20 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_user_image_alter_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل'),
        ),
    ]