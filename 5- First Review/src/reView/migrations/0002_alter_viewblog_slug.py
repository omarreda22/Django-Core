# Generated by Django 4.1.1 on 2022-10-04 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reView', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewblog',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]