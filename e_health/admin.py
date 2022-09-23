from django.contrib import admin
from .models import DadosPaciente, Pacientes

admin.site.register(Pacientes)
admin.site.register(DadosPaciente)
