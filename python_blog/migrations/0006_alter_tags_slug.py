# Generated by Django 5.1.4 on 2025-01-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_blog', '0005_alter_tags_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
