# Generated by Django 4.2.4 on 2023-09-02 18:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("document_flow", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="caddocument",
            old_name="project_number",
            new_name="project",
        ),
    ]
