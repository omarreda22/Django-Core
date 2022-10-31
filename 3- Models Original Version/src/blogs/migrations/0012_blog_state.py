# Generated by Django 4.1.1 on 2022-09-12 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_alter_blog_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='state',
            field=models.CharField(choices=[('DR', 'Draft'), ('PU', 'Public'), ('PR', 'Private')], default='DR', max_length=120),
        ),
    ]