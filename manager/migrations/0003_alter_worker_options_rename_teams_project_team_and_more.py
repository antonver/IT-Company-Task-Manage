# Generated by Django 5.1.1 on 2024-10-08 19:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0002_alter_worker_position"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="worker",
            options={
                "ordering": ["position"],
                "verbose_name": "worker",
                "verbose_name_plural": "workers",
            },
        ),
        migrations.RenameField(
            model_name="project",
            old_name="teams",
            new_name="team",
        ),
        migrations.AlterField(
            model_name="worker",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="workers",
                to="manager.team",
            ),
        ),
    ]
