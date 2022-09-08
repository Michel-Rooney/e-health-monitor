from email.policy import default
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
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
        try:
            foto_perfil = request.FILES['foto-perfil']
        except:
            foto_perfil = None

        if empty_field(request, nome, sexo, idade, email, telefone):
            return redirect('/pacientes')

        if not name_is_valid(request, nome):
            return redirect('/pacientes')

        if not idade_is_valid(request, idade):
            return redirect('/pacientes')
            
        if paciente_exist(request, email):
            return redirect('/pacientes')

        try:
            paciente = Pacientes(nome=nome, sexo=sexo, idade=idade, email=email, 
                                telefone=telefone, medico=request.user, foto_perfil=foto_perfil)
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso')
            return redirect('/pacientes')
        except:
            messages.error(request, 'Erro interno do sistema')
            return redirect('/pacientes')

@login_required(login_url='/auth/logar')
def dados_paciente_listar(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.filter(medico=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes':pacientes})

@login_required(login_url='/auth/logar')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.medico == request.user:
        messages.error(request, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == 'GET':
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente':paciente, 'dados_paciente':dados_paciente})
    elif request.method == 'POST':
        peso = request.POST['peso']
        altura = request.POST['altura']
        gordura = request.POST['gordura']
        musculo = request.POST['musculo']

        hdl = request.POST['hdl']
        ldl = request.POST['ldl'] 
        colesterol_total = request.POST['ctotal']
        trigliceridios = request.POST['triglicerídios']

        try:
            paciente = DadosPaciente(paciente=paciente, data=datetime.now(), peso=peso,
                                    altura=altura, percentual_gordura=gordura, percentual_musculo=musculo,
                                    colesterol_hdl=hdl, colesterol_ldl=ldl, colesterol_total=colesterol_total,
                                    trigliceridios=trigliceridios)

            paciente.save()
            messages.success(request, 'Dados cadastrados com sucesso')
            return redirect('/pacientes/')
        except:
            messages.error(request, 'Não foi possivel cadastrar os dados')
            return redirect('/pacientes/')

@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by('data')

    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos, 'labels':labels}
    return JsonResponse(data)

def plano_alimentar_listar(request):
    if request.method == 'GET':
        pacientes = Pacientes.objects.filter(medico=request.user)    
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})

def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.medico == request.user:
        messages.error(request, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar')

    if request.method == "GET":
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao' : opcao})



def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.medico == request.user:
        messages.error(request, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        r1.save()

        messages.success(request, 'Refeição cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')


def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.success(request, 'Opcao cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')
    