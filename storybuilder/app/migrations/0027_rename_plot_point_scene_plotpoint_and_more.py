# Generated by Django 5.0.6 on 2024-12-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_alter_plotpoint_order_alter_scene_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scene',
            old_name='plot_point',
            new_name='plotpoint',
        ),
        migrations.AlterField(
            model_name='plotpoint',
            name='order',
            field=models.SmallIntegerField(blank=True, default=1),
        ),
        migrations.AlterField(
            model_name='scene',
            name='order',
            field=models.SmallIntegerField(blank=True, default=1),
        ),
    ]
