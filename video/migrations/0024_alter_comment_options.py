# Generated by Django 4.1 on 2022-09-18 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0023_alter_tag_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-video__id', 'parent__id'], 'verbose_name': 'کامنت', 'verbose_name_plural': 'کامنت\u200cها'},
        ),
    ]
