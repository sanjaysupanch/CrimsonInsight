# Generated by Django 2.2.1 on 2020-01-24 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200123_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releaseapk',
            name='email_field',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]