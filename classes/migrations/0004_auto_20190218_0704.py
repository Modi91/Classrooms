# Generated by Django 2.1.5 on 2019-02-18 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1),
        ),
    ]