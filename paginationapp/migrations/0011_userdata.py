# Generated by Django 4.1.9 on 2023-07-12 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginationapp', '0010_alter_book_views_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.TextField(default=None)),
            ],
        ),
    ]
