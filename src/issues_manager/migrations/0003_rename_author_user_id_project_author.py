# Generated by Django 4.0.3 on 2022-04-11 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issues_manager', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='author_user_id',
            new_name='author',
        ),
    ]