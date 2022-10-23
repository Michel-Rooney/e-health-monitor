from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    STATUS = (
        ('M', 'Médico'),
        ('P', 'Paciente'),
        ('A', 'Administrador')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nivel = models.CharField(max_length=1, choices=STATUS, default='P')

    def __str__(self) -> str:
        return self.user.username