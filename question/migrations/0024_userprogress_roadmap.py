# Generated by Django 4.2.11 on 2025-03-22 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0023_userprogress_remove_usersolvedquestion_question_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='roadmap',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='question.roadmap'),
        ),
    ]
