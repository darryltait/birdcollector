# Generated by Django 3.1.6 on 2021-02-19 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20210219_0907'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='toy',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='bird',
            name='toys',
            field=models.ManyToManyField(to='main_app.Toy'),
        ),
    ]
