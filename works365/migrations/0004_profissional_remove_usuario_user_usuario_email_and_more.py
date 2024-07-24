# Generated by Django 5.0.6 on 2024-06-20 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works365', '0003_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(default=1, max_length=255)),
                ('telefone', models.CharField(default=1, max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('areas_atuacao', models.TextField()),
                ('senha', models.CharField(default=1, max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='user',
        ),
        migrations.AddField(
            model_name='usuario',
            name='email',
            field=models.EmailField(default=1, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nome_completo',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='senha',
            field=models.CharField(default=1, max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefone',
            field=models.CharField(default=1, max_length=15),
        ),
    ]
