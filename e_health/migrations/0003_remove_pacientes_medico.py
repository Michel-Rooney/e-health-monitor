# Generated by Django 4.1 on 2022-10-22 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_health', '0002_alter_pacientes_medico'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pacientes',
            name='medico',
        ),
    ]
