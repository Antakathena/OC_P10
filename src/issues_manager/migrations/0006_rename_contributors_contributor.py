# Generated by Django 4.0.3 on 2022-04-26 15:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('issues_manager', '0005_rename_project_id_issue_project_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Contributors',
            new_name='Contributor',
        ),
    ]