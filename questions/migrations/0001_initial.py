# Generated by Django 3.1.3 on 2021-05-10 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quizes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=220)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizes.quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=220)),
                ('correto', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('questao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respostas', to='questions.questao')),
            ],
        ),
    ]
