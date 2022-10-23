# Generated by Django 4.1 on 2022-10-22 23:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('e_health', '0004_remove_pacientes_user_pacientes_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacientes',
            name='medico',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]