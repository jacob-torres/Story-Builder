# Generated by Django 5.0.6 on 2024-11-09 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(blank=True, max_length=100)),
                ('age', models.PositiveSmallIntegerField(null=True)),
                ('ethnicity', models.CharField(blank=True, max_length=100)),
                ('occupation', models.CharField(blank=True, max_length=100)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('hair_color', models.CharField(blank=True, max_length=100)),
                ('eye_color', models.CharField(blank=True, max_length=100)),
                ('height', models.CharField(blank=True, max_length=100)),
                ('body_type', models.CharField(blank=True, max_length=100)),
                ('mbti_personality', models.CharField(choices=[('INTJ', 'INTJ: The Architect'), ('INTP', 'INTP: The Logician'), ('ENTJ', 'ENTJ: The Commander'), ('ENTP', 'ENTP: The Visionary'), ('INFJ', 'INFJ: The Advocate'), ('INFP', 'INFP: The Idealist'), ('ENFJ', 'ENFJ: The Giver'), ('ENFP', 'ENFP: The Enthusiast'), ('ISTJ', 'ISTJ: The Duty Fulfiller'), ('ISFJ', 'ISFJ: The Protector'), ('ESTJ', 'ESTJ: The Executive'), ('ESFJ', 'ESFJ: The Caregiver'), ('ISTP', 'ISTP: The Craftsman'), ('ISFP', 'ISFP: The Artist')], null=True)),
                ('enneagram_personality', models.CharField(choices=[('1', '1: The Reformer'), ('2', '2: The Helper'), ('3', '3: The Achiever'), ('4', '4: The Romantic'), ('5', '5: The Investigator'), ('6', '6: The Skeptic'), ('7', '7: The Enthusiast'), ('8', '8: The Challenger'), ('9', '9: The Peacemaker')], null=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('characters', models.ManyToManyField(to='app.character')),
            ],
        ),
        migrations.CreateModel(
            name='PlotPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('scenes', models.ManyToManyField(to='app.scene')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('premise', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('genre', models.CharField(blank=True, max_length=100)),
                ('word_count', models.PositiveIntegerField(default=0)),
                ('date_started', models.DateField(auto_now_add=True)),
                ('date_last_saved', models.DateField(auto_now=True)),
                ('date_finished', models.DateField(null=True)),
                ('characters', models.ManyToManyField(to='app.character')),
            ],
        ),
        migrations.AddField(
            model_name='scene',
            name='story',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.story'),
        ),
        migrations.CreateModel(
            name='Plot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('plot_points', models.ManyToManyField(to='app.plotpoint')),
                ('stories', models.ManyToManyField(to='app.story')),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('stories', models.ManyToManyField(to='app.story')),
            ],
        ),
        migrations.CreateModel(
            name='World',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('characters', models.ManyToManyField(to='app.character')),
                ('stories', models.ManyToManyField(to='app.story')),
            ],
        ),
    ]
