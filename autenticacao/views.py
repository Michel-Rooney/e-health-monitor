from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .utils import *

def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, 'Você não pode acessar a página de cadastro estando logado')
            return redirect('/')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST['usuario']
        email = request.POST['email']
        password = request.POST['senha']
        confirm_password = request.POST['confirmar_senha']

        if not user_is_valid(request, username):
            return redirect('/auth/cadastro')
        if not email_is_valid(request, email):
            return redirect('/auth/cadastro')
        if not password_is_valid(request, password, confirm_password):
            return redirect('/auth/cadastro')            

        try:
            user = User.objects.create_user(username=username, email=email,
                                            password=password)
            user.save()
            messages.success(request, 'Usuário cadastrado com sucesso')
            return redirect('/auth/logar')
        except:
            messages.error(request, 'Error interno do sistema')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.info(request, 'Você não pode acessar a página de login estando logado')
            return redirect('/')
        return render(request, 'logar.html')
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Usuário ou seja inválidos')
            return redirect('/auth/logar')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')