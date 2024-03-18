# Generated by Django 5.0.3 on 2024-03-18 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Respondents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=36, unique=True)),
                ('sex', models.CharField(max_length=1)),
                ('age', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SampleMetaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=36, unique=True)),
                ('speaker_name', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=100)),
                ('sample_name', models.CharField(max_length=100)),
                ('kind', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naturalness', models.SmallIntegerField()),
                ('intelligibility', models.SmallIntegerField()),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.respondents')),
                ('sample_meta_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.samplemetadata')),
            ],
        ),
    ]