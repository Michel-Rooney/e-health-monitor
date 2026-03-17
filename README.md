# 🏥 E-Health Monitor

Sistema web de monitoramento de saúde para clínicas e consultórios. Permite que médicos acompanhem os dados clínicos de seus pacientes — como peso, composição corporal e colesterol — com histórico e visualização em gráficos.

---

## 🚀 Tecnologias

| Tecnologia | Versão |
|---|---|
| Python | 3.x |
| Django | 4.2.17 |
| SQLite | (desenvolvimento) |
| PostgreSQL | (produção via Heroku) |
| Pillow | 10.3.0 |
| Gunicorn | 23.0.0 |
| WhiteNoise | 6.2.0 |
| django-heroku | 0.3.1 |

---

## 🗂️ Estrutura do Projeto

```
e-health-monitor/
├── core/                   # Configurações principais (settings, urls, wsgi/asgi)
├── autenticacao/           # Cadastro, login e logout de usuários
│   ├── models.py           # Model Usuario com níveis de acesso
│   ├── views.py            # Views de cadastro, login e logout
│   └── urls.py             # Rotas de autenticação
├── e_health/               # App principal da plataforma
│   ├── models.py           # Pacientes e DadosPaciente
│   ├── views.py            # Dashboard, pacientes, dados e gráficos
│   ├── urls.py             # Rotas da plataforma
│   └── utils.py            # Validações de formulário
├── templates/              # Templates HTML e arquivos estáticos globais
├── media/                  # Uploads de fotos de perfil dos pacientes
├── manage.py
├── requirements.txt
└── Procfile                # Configuração para deploy no Heroku
```

---

## 👥 Níveis de Acesso

O sistema possui três tipos de usuário, definidos no model `Usuario`:

| Nível | Código | Permissões |
|---|---|---|
| Paciente | `P` | Visualiza e cadastra seus próprios dados clínicos |
| Médico | `M` | Monitora pacientes, visualiza e registra dados de saúde |
| Administrador | `A` | Pode promover pacientes a médicos |

---

## 🌐 Rotas

### 🔐 Autenticação — `/auth/`

| URL | Método | Descrição | Login |
|---|---|---|---|
| `/auth/cadastro/` | GET / POST | Formulário de criação de conta | ❌ |
| `/auth/logar/` | GET / POST | Login na plataforma | ❌ |
| `/auth/sair/` | GET | Logout e redirecionamento | ✅ |

> Usuários já autenticados são redirecionados ao tentar acessar as páginas de cadastro ou login.

---

### 🏠 Plataforma — `/`

| URL | Método | Descrição | Login |
|---|---|---|---|
| `/` | GET / POST | Página inicial com formulário de contato | ❌ |
| `/cadastro_info/` | GET / POST | Completar perfil do paciente após primeiro login | ✅ |
| `/pacientes/` | GET / POST | Lista de pacientes disponíveis e monitorados | ✅ (Médico/Admin) |
| `/dados_paciente/{id}/` | GET / POST | Visualizar e registrar dados clínicos de um paciente | ✅ |
| `/grafico_peso/{id}/` | GET | Retorna JSON com histórico de peso para o gráfico | ✅ |
| `/torna_medico/` | POST | Promove um paciente ao nível de médico | ✅ (Admin) |
| `/cancelar_monitoriamento/{id}/` | GET | Remove vínculo médico-paciente | ✅ (Médico) |

---

## 📊 Dados Clínicos Monitorados

Cada registro de `DadosPaciente` armazena:

| Campo | Descrição |
|---|---|
| `peso` | Peso (kg) |
| `altura` | Altura (cm) |
| `percentual_gordura` | % de gordura corporal |
| `percentual_musculo` | % de massa muscular |
| `colesterol_hdl` | Colesterol HDL (bom) |
| `colesterol_ldl` | Colesterol LDL (ruim) |
| `colesterol_total` | Colesterol total |
| `trigliceridios` | Triglicerídios |
| `data` | Data/hora do registro |

O histórico de peso é exibido em gráfico na tela do paciente, consumindo o endpoint `/grafico_peso/{id}/`.

---

## ✉️ Formulário de Contato

A página inicial possui um formulário de contato que envia um e-mail HTML para o administrador via SMTP. Requer as seguintes variáveis de ambiente:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/Michel-Rooney/e-health-monitor.git
cd e-health-monitor
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY='sua-chave-secreta-django'

EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Acesse em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🚢 Deploy (Heroku)

O projeto está configurado para deploy no Heroku com `django-heroku` e `Procfile`:

```
web: gunicorn core.wsgi
```

Para fazer o deploy:

```bash
heroku create nome-do-app
git push heroku main
heroku run python manage.py migrate
```

Configure as variáveis de ambiente no painel do Heroku ou via CLI:

```bash
heroku config:set SECRET_KEY='...' EMAIL_HOST='...' ...
```

---

## ✒️ Autor

* [Michel-Rooney](https://github.com/Michel-Rooney/) — Dev. Backend
