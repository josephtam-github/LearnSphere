# Generated by Django 4.2.18 on 2025-03-09 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField()),
                ('regions', models.JSONField(default=list)),
            ],
            options={
                'db_table': 'language',
            },
        ),
        migrations.CreateModel(
            name='LearningModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('order', models.IntegerField()),
                ('is_active', models.BooleanField(default=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules', to='learningCore.language')),
            ],
            options={
                'db_table': 'learning_module',
                'ordering': ['language', 'order'],
                'unique_together': {('language', 'order')},
            },
        ),
        migrations.CreateModel(
            name='LearningActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('activity_type', models.CharField(choices=[('vocabulary', 'Vocabulary Learning'), ('listening', 'Listening Exercise'), ('speaking', 'Speaking Practice'), ('quiz', 'Quiz'), ('game', 'Interactive Game'), ('story', 'Story Reading'), ('culture', 'Cultural Learning')], max_length=30)),
                ('content', models.JSONField()),
                ('points', models.IntegerField(default=10)),
                ('estimated_time_minutes', models.IntegerField(default=5)),
                ('is_premium', models.BooleanField(default=False)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activities', to='learningCore.learningmodule')),
            ],
            options={
                'db_table': 'learning_activity',
                'ordering': ['module', 'id'],
            },
        ),
    ]
