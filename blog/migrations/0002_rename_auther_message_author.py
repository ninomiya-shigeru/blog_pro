# Generated by Django 3.2.1 on 2024-12-29 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='auther',
            new_name='author',
        ),
    ]
