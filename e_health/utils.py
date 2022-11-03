from django.contrib import messages
from .models import Pacientes

def empty_field(request, sexo, idade, telefone):
    # if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
    if (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(telefone.strip()) == 0):
        messages.error(request, 'Preencha todos os campos')
        return True
    return False

# def name_is_valid(request, nome):
#     if len(nome) > 50:
#         messages.error(request, 'O nome so pode ter no máximo 50 caracteres')
#         return False
#     return True

def idade_is_valid(request, idade):
    if not idade.isnumeric():
        messages.error(request, 'Digite uma idade válida')
        return False
    elif int(idade) <= 0 or int(idade) > 150:
        messages.error(request, 'Olá ser superior. Digita uma idade válida espertinho')
        return False
    return True

# def paciente_exist(request, email):
#     paciente = Pacientes.objects.filter(email=email)
#     if paciente.exists():
#         messages.error(request, 'Já existe um paciente com esse E-mail')
#         return True
#     return False
