# Generated by Django 5.0.6 on 2024-09-15 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_user_profile_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_img_base64',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]