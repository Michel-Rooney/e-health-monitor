from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes
from .utils import *
from datetime import datetime


@login_required(login_url='/auth/logar')
def pacientes(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.filter(medico=request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == 'POST':
        nome = request.POST['nome']
        sexo = request.POST['sexo']
        idade = request.POST['idade']
        email = request.POST['email']
        telefone = request.POST['telefone']

        if empty_field(request, nome, sexo, idade, email, telefone):
            return redirect('/pacientes')

        if not idade_is_valid(request, idade):
            return redirect('/pacientes')
            
        if paciente_exist(request, email):
            return redirect('/pacientes')

        try:
            paciente = Pacientes(nome=nome, sexo=sexo, idade=idade, email=email, 
                                telefone=telefone, medico=request.user)
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso')
            return redirect('/pacientes')
        except:
            messages.error(request, 'Erro interno do sistema')
            return redirect('/pacientes')

def dados_paciente_listar(request):
    pass

def plano_alimentar_listar(request):
    pass
