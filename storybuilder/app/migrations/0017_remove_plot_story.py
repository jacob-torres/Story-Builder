# Generated by Django 5.0.6 on 2024-12-08 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_remove_story_plot_plot_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plot',
            name='story',
        ),
    ]
