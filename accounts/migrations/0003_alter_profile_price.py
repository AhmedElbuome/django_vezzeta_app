# Generated by Django 4.2.7 on 2023-12-02 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='سعر الكشف :'),
        ),
    ]