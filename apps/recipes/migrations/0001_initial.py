# Generated by Django 4.2.14 on 2024-08-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ingredients', models.CharField(help_text='Enter ingredients comma separated', max_length=255)),
                ('cooking_time', models.IntegerField(help_text='Enter cooking time (minutes)')),
                ('difficulty', models.CharField(max_length=20)),
            ],
        ),
    ]
