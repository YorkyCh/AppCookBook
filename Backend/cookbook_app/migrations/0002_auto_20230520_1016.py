# Generated by Django 3.2.18 on 2023-05-20 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='category',
        ),
        migrations.AddField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(to='cookbook_app.Category'),
        ),
    ]
