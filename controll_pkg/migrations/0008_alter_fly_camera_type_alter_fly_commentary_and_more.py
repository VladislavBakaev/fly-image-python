# Generated by Django 4.0.3 on 2022-05-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('controll_pkg', '0007_alter_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fly',
            name='camera_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='fly',
            name='commentary',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='fly',
            name='robot_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
