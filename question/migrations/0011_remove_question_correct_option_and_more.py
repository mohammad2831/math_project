from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0010_userscore'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_option',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option1_image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option1_image_basa64',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option1_title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option2_image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option2_image_basa64',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option2_title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option3_image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option3_image_basa64',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option3_title',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option4_image',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option4_image_basa64',
        ),
        migrations.RemoveField(
            model_name='question',
            name='option4_title',
        ),
        migrations.AddField(
            model_name='question',
            name='img',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='question',
            name='img_base64',
            field=models.TextField(null=True),
        ),
    ]
