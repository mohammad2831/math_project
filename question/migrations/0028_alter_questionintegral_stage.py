# Generated by Django 5.2 on 2025-04-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0027_alter_questionderivative_stage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionintegral',
            name='stage',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]
