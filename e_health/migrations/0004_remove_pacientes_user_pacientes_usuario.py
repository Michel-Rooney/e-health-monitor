# Generated by Django 4.1 on 2022-10-22 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0001_initial'),
        ('e_health', '0003_remove_pacientes_medico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientes',
            name='user',
        ),
        migrations.AddField(
            model_name='pacientes',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autenticacao.usuario'),
        ),
    ]
