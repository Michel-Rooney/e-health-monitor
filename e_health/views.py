from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Pacientes, DadosPaciente
from .utils import *
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from autenticacao.models import Usuario


def index(request):
    try:
        usuario = Usuario.objects.get(user=request.user.id)
    except:
        usuario = None
    if request.method == 'GET':
        return render(request, 'index.html', {'usuario':usuario})
    elif request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        numero = request.POST['numero']
        mensagem = request.POST['mensagem']

        html_content = render_to_string('emails/contate_me.html', {
            'nome' : nome, 'email': email, 'numero': numero, 'mensagem': mensagem 
        })
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives('Contate-me', text_content, settings.EMAIL_HOST_USER, ['michelrooney16@gmail.com',])
        email.attach_alternative(html_content, 'text/html')
        email.send()

        messages.success(request, 'Conta-me enviando com sucesso')
        return redirect('/')

@login_required(login_url='/auth/logar')
def pacientes(request):
    user = Usuario.objects.get(user=request.user.id)
    if request.method == 'GET':
        if user.nivel == 'P':
            messages.warning(request, 'Você não tem permisão para acessar essa pagina')
            return redirect(f'/dados_paciente/{request.user.id}')
        else:
            # pacs = Pacientes.objects.filter(medico=None)
            # pacientes = Pacientes.objects.filter(medico=request.user)

            pacientes_user = Pacientes.objects.filter(medico=user.id).exclude(usuario=user)
            pacientes = Pacientes.objects.filter(medico=None).exclude(usuario=user)

            return render(request, 'pacientes.html', {'user':user, 'pacientes_user':pacientes_user, 'pacientes':pacientes})
    elif request.method == 'POST':
        pac = request.POST['paciente']

        try:
            paciente = Pacientes.objects.get(usuario=pac)
            paciente.medico = request.user
            paciente.save()
            messages.success(request, 'Paciente agora está sendo monitorado')
            return redirect(f'/pacientes')
        except:
            messages.error(request, 'Não foi possivel monitorar esse paciente')
            return redirect(f'/pacientes')

@login_required(login_url='/auth/logar')
def dados_paciente(request, id):
    # user = get_object_or_404(Usuario, id=id)
    # paciente = Pacientes.objects.get(usuario=user)
    # usuarios = Usuario.objects.filter(nivel='P')
    # if not paciente.medico == request.user:
    #     messages.error(request, 'Esse paciente não é seu')
    #     return redirect('/dados_paciente/')

    # usr = Usuario.objects.get(user=request.user)
    # pac = Pacientes.objects.get(usuario=id)

    # print(f'01 {request.user.username}')
    # print(f'02 {pac.medico}')

    # print(usr)
    # print(pac)

    user = Usuario.objects.get(user=request.user.id)
    paciente_user = Usuario.objects.get(id=id)
    paciente = Pacientes.objects.get(usuario=paciente_user)
    dados_paciente = DadosPaciente.objects.filter(paciente=paciente.id)
    all_pacientes = Pacientes.objects.all().exclude(usuario=user.id)

    print(user)
    print(paciente.medico)

    if request.method == 'GET':
        if user.id == paciente.usuario.id:
            return render(request, 'dados_paciente.html', {'user':user, 'paciente':paciente, 'dados_paciente':dados_paciente, 'all_pacientes':all_pacientes})
        elif str(user) != str(paciente.medico):
            messages.error(request, 'Você não tem permissão para acessar está página')
            return redirect(f'/pacientes')
        return render(request, 'dados_paciente.html', {'user':user, 'paciente':paciente, 'dados_paciente':dados_paciente, 'all_pacientes':all_pacientes})

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
            dados = DadosPaciente(paciente=paciente, data=datetime.now(), peso=peso,
                                    altura=altura, percentual_gordura=gordura, percentual_musculo=musculo,
                                    colesterol_hdl=hdl, colesterol_ldl=ldl, colesterol_total=colesterol_total,
                                    trigliceridios=trigliceridios)

            dados.save()
            messages.success(request, 'Dados cadastrados com sucesso')
            return redirect(f'/dados_paciente/{paciente.usuario.id}')   
        except:
            messages.error(request, 'Não foi possivel cadastrar os dados')
            return redirect(f'/dados_paciente/{paciente.usuario.id}')

@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by('data')

    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos, 'labels':labels}
    return JsonResponse(data)


@login_required(login_url='/auth/logar')
def cadastro_info(request):
    user = Usuario.objects.get(user=request.user.id)
    try:
        paciente = Pacientes.objects.get(usuario=user.id)
    except:
        paciente = False
    if request.method == 'GET':
        if paciente:
            return redirect(f'/dados_paciente/{user.id}')
        return render(request, 'cadastro_info.html')
    elif request.method == 'POST':
        
        sexo = request.POST['sexo']
        idade = request.POST['idade']
        telefone = request.POST['telefone']

        try:
            foto_perfil = request.FILES['foto-perfil']
        except:
            foto_perfil = None

        if empty_field(request, sexo, idade, telefone):
            return redirect('/pacientes')


        if not idade_is_valid(request, idade):
            return redirect('/pacientes')
        print(user)
        print(user.id)
        print(user.user.username)
        print(user.user.email)

        try:
            paciente = Pacientes(usuario=user, nome=user.user.username, sexo=sexo, idade=idade, email=user.user.email, 
                                telefone=telefone, foto_perfil=foto_perfil)
            paciente.save()
            messages.success(request, 'Paciente cadastrado com sucesso')
            return redirect(f'/dados_paciente/{user.id}')
        except:
            messages.error(request, 'Erro interno do sistema')
            return redirect('/cadastro_info')


def torna_medico(request):
    usuario = request.POST['usuarios']

    try:
        user = Usuario.objects.get(user=usuario)
        user.nivel = 'M'
        user.save()
        messages.success(request, 'Agora o paciente selecionado é médico')
        u = Usuario.objects.get(user=request.user.id)
        return redirect(f'/dados_paciente/{u.id}')
    except:
        messages.error(request, 'Não foi possivel torna esse paciente um médico ')
        return redirect(f'/dados_paciente/{u.id}')


def cancelar_monitoriamento(request, id):
    paciente = Pacientes.objects.get(id=id)
    paciente.medico = None
    paciente.save()
    return redirect('/pacientes')
