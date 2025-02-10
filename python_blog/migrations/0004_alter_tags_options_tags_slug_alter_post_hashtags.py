# Generated by Django 5.1.4 on 2025-01-13 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_blog', '0003_alter_post_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tags',
            options={'ordering': ['name'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AddField(
            model_name='tags',
            name='slug',
            field=models.SlugField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(blank=True, related_name='posts', to='python_blog.tags', verbose_name='Теги'),
        ),
    ]
