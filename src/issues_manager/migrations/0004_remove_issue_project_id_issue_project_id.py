# Generated by Django 4.0.3 on 2022-04-15 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues_manager', '0003_rename_author_user_id_project_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='project_id',
        ),
        migrations.AddField(
            model_name='issue',
            name='Project_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projet_associe', to='issues_manager.project'),
            preserve_default=False,
        ),
    ]