# Generated by Django 4.0.3 on 2022-04-26 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controll_pkg', '0004_alter_fly_at_fly'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fly',
            name='at_fly',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
