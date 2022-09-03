# Generated by Django 4.1 on 2022-09-03 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_health', '0002_rename_percentural_gordura_dadospacientes_percentual_gordura_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DadosPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('peso', models.IntegerField()),
                ('altura', models.IntegerField()),
                ('percentual_gordura', models.IntegerField()),
                ('percentual_musculo', models.IntegerField()),
                ('colesterol_hdl', models.IntegerField()),
                ('colesterol_ldl', models.IntegerField()),
                ('colesterol_total', models.IntegerField()),
                ('trigliceridios', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='opcao')),
                ('descricao', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Refeicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('horario', models.TimeField()),
                ('carboidratos', models.IntegerField()),
                ('proteinas', models.IntegerField()),
                ('gorduras', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='pacientes',
            name='sexo',
            field=models.CharField(choices=[('F', 'Feminino'), ('M', 'Maculino')], max_length=1),
        ),
        migrations.DeleteModel(
            name='DadosPacientes',
        ),
        migrations.AddField(
            model_name='refeicao',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_health.pacientes'),
        ),
        migrations.AddField(
            model_name='opcao',
            name='refeicao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_health.refeicao'),
        ),
        migrations.AddField(
            model_name='dadospaciente',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_health.pacientes'),
        ),
    ]
