# Generated by Django 5.0.6 on 2024-11-17 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_plot_plot_points_remove_plot_stories_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='genre',
            new_name='genres',
        ),
        migrations.AlterField(
            model_name='story',
            name='premise',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
