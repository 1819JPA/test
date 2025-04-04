# Generated by Django 5.1.6 on 2025-03-25 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listing_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image', models.URLField(blank=True, null=True)),
                ('description', models.TextField()),
                ('private', models.BooleanField()),
                ('properties', models.ManyToManyField(to='listing_service.property')),
            ],
        ),
    ]
