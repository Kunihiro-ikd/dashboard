# Generated by Django 4.0 on 2023-02-10 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cnn', '0003_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='gray',
        ),
        migrations.RemoveField(
            model_name='document',
            name='photo',
        ),
        migrations.AddField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/'),
        ),
    ]
