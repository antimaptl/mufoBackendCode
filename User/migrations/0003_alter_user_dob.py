# Generated by Django 4.2.2 on 2025-06-13 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_alter_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='Dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
