# Generated by Django 4.0.6 on 2022-11-25 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postitApp', '0012_comment_post_comment_user_alter_comment_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='text',
        ),
    ]
