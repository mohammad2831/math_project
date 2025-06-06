# Generated by Django 5.2 on 2025-04-27 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0025_remove_userprogress_completed_questions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionIntegral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('question_latex', models.TextField(blank=True, null=True)),
                ('description', models.TextField(null=True)),
                ('stage', models.SmallIntegerField(null=True)),
                ('score', models.SmallIntegerField(blank=True, null=True)),
                ('difficulty', models.CharField(choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')], max_length=6, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Question',
            new_name='QuestionDerivative',
        ),
        migrations.RenameModel(
            old_name='Stage',
            new_name='StageDerivative',
        ),
        migrations.CreateModel(
            name='StageIntegral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_number', models.PositiveIntegerField()),
                ('option1_title', models.CharField(default='', max_length=255)),
                ('option1_latex', models.TextField(blank=True, null=True)),
                ('option1_descrption', models.TextField(blank=True, null=True)),
                ('option2_title', models.CharField(default='', max_length=255)),
                ('option2_latex', models.TextField(blank=True, null=True)),
                ('option2_descrption', models.TextField(blank=True, null=True)),
                ('option3_title', models.CharField(default='', max_length=255)),
                ('option3_latex', models.TextField(blank=True, null=True)),
                ('option3_descrption', models.TextField(blank=True, null=True)),
                ('option4_title', models.CharField(default='', max_length=255)),
                ('option4_latex', models.TextField(blank=True, null=True)),
                ('option4_descrption', models.TextField(blank=True, null=True)),
                ('correct_option', models.CharField(default='1', max_length=255)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stages', to='question.questionintegral')),
            ],
        ),
        migrations.DeleteModel(
            name='Roadmap',
        ),
    ]
