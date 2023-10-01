# Generated by Django 4.2.5 on 2023-09-30 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tokens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_url', models.URLField(unique=True)),
                ('short_url', models.CharField(blank=True, db_index=True, max_length=20, unique=True)),
                ('requests_count', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created_date',),
            },
        ),
    ]
