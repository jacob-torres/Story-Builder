# Generated by Django 5.0.6 on 2024-12-08 22:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_remove_plot_story'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='plot',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='story', to='app.plot'),
        ),
    ]
