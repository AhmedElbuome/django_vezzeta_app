# Generated by Django 4.2.7 on 2023-12-07 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_appointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='additional_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]