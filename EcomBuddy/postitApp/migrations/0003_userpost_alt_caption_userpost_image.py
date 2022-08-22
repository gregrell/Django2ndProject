# Generated by Django 4.1 on 2022-08-21 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postitApp', '0002_alter_userpost_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='alt_caption',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='userpost',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]