from django.contrib import messages
from django.contrib.auth.models import User
import re


def user_is_valid(request, username):
    if username == '':
        messages.error(request, 'O campo do usuário está vazio')
        return False
    try:
        user = User.objects.get(username=username)
        messages.error(request, 'Já existe um usuário com esse nome')
        return False
    except:
        return True

def email_is_valid(request, email):
    if email == '':
        messages.error(request, 'O campo do email está vazio')
        return False
    try:
        email = User.objects.get(email=email)
        messages.error(request, 'Já existe um usuário com esse email')
        return False
    except:
        return True


def password_is_valid(request, password, confirm_password):
    if password == '':
        messages.error(request, 'O campo de senha está vazio')
        return False
    elif len(password) <= 5:
        messages.error(request, 'A senha precisa ser maior que 5 caracteres')
        return False
    elif not password == confirm_password:
        messages.error(request, 'As senhas não coicidem')
        return False
    elif not re.search('[A-Z]', password):
        messages.error(request, 'A senha precisar ter letras maiusculas')
        return False
    elif not re.search('[a-z]', password):
        messages.error(request, 'A senha precisar ter letras minusculas')
        return False
    elif not re.search('[0-9]', password):
        messages.error(request, 'A senha precisa conter números')
        return False

    return True

        