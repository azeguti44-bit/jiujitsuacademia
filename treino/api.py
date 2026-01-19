# @treino_router.post('', response={200: AlunoSchema})
# def criar_aluno(request, aluno_schema: AlunoSchema):    
#     nome = aluno_schema.dict()['nome']
#     email = aluno_schema.dict()['email']
#     faixa = aluno_schema.dict()['faixa']
#     data_nascimento = aluno_schema.dict()['data_nascimento']

#     if Alunos.objects.filter(email=email).exists():
#         raise HttpError(400, "Email já cadastrado")
    
#     aluno = Alunos(
#             nome=nome,
#             email = email,
#             faixa = faixa,
#             data_nascimento = data_nascimento,
#             )
    
#     aluno.save()

#     return aluno

from ninja import Router
from .schemas import  ProgressoAlunoSchema, AulaRealizadaSchema, HistoricoCompletoSchema, LoginSchema, AlunoOutSchema, AlunoInSchema, AlunoUpdateSchema
from .models import Alunos, AulasConcluidas
from ninja.errors import HttpError
from typing import List
from .graduacao import *
from datetime import date
from ninja.security import HttpBearer
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate

treino_router = Router()

class InvalidToken(HttpError):
    pass

class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        # Aqui você verificaria o JWT. Para simplificar no início, 
        # vamos simular que o token é o username do usuário.
        try:
            user = User.objects.get(username=token)
            return user
        except User.DoesNotExist:
            return None


@treino_router.post('/cadastro_aluno/', response={200: AlunoOutSchema})
def cadastro_aluno(request, aluno_schema: AlunoInSchema):
    if Alunos.objects.filter(email=aluno_schema.email).exists():
        raise HttpError(400, "Este e-mail já está cadastrado.")

    with transaction.atomic():
        # 1. Cria o User do Django para autenticação
        user = User.objects.create_user(
            username=aluno_schema.email,
            email=aluno_schema.email,
            password=aluno_schema.password
        )

        # 2. Cria o Aluno vinculado ao User
        aluno = Alunos.objects.create(
            usuario=user,
            nome=aluno_schema.nome,
            email=aluno_schema.email,
            faixa=aluno_schema.faixa,
            data_nascimento=aluno_schema.data_nascimento
        )

    return aluno

@treino_router.post('/login/', auth=None) # auth=None pois o aluno ainda não logou
def login(request, data: LoginSchema):
    # O Django verifica se o e-mail e a senha batem com o User criado no cadastro
    user = authenticate(username=data.email, password=data.senha)

    if user is not None:
        # Retornamos o username (e-mail) que o seu GlobalAuth espera como token
        return {"token": user.username, "mensagem": "Login bem-sucedido"}
    else:
        raise HttpError(401, "E-mail ou senha inválidos")



@treino_router.get('/aluno/', response=List[AlunoOutSchema], auth=GlobalAuth())
def listar_alunos(request):
        if not request.auth.is_staff:
            raise HttpError(403, "Apenas instrutores podem cadastrar alunos.")
     
        alunos = Alunos.objects.all()
        return alunos

@treino_router.get('/progresso_aluno/', response={200:ProgressoAlunoSchema}, auth=GlobalAuth())
def progresso_aluno(request, email_aluno: str):
    if not request.auth.is_staff:
        raise HttpError(403, "Apenas instrutores podem cadastrar alunos.")
    
    aluno = Alunos.objects.get(email = email_aluno)
    faixa_atual = aluno.get_faixa_display()
    n = order_belt.get(faixa_atual, 0)
    total_aulas_proxima_faixa = calculate_lesson_to_upgrade(n)
    total_aulas_concluidas_faixa_atual = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa).count()
    aulas_que_faltam = total_aulas_proxima_faixa - total_aulas_concluidas_faixa_atual

    return {

            "email": aluno.email,
            "nome": aluno.nome,
            "faixa": faixa_atual,
            "total_aulas": total_aulas_concluidas_faixa_atual,
            "aulas_necessarias_para_proxima_faixa": aulas_que_faltam,

        }

@treino_router.post('/aula_realizada/', response={200: str}, auth=GlobalAuth())
def aula_realizada(request, aula_done: AulaRealizadaSchema):
    if not request.auth.is_staff:
        raise HttpError(403, "Apenas instrutores podem cadastrar alunos.")
    
    qtd = aula_done.dict()['qtd']
    email_aluno = aula_done.dict()['email_aluno']

    if qtd <= 0:
        raise HttpError (400, "Quantidade de aulas incompatível")
    
    aluno = Alunos.objects.get(email=email_aluno)

    for i in range(0, qtd):
        ac = AulasConcluidas(
            aluno = aluno,
            faixa_atual = aluno.faixa
        )

        ac.save()

    return 200, f"Aula marcada como realizada pelo aluno {aluno.nome}"

@treino_router.put('/aluno/{aluno_id}/', response=AlunoOutSchema, auth=GlobalAuth())
def update_aluno(request, aluno_id: int, aluno_data: AlunoUpdateSchema):
    if not request.auth.is_staff:
        raise HttpError(403, "Apenas instrutores podem cadastrar alunos.")
    
    aluno = Alunos.objects.get(id=aluno_id)
    idade = (date.today() - aluno.data_nascimento).days // 365

    if idade < 18 and aluno_data.faixa in ('A', 'R', 'M', 'P'):
        raise HttpError(400, 'Menores de idade não podem receber essa faixa')
    
    # modo mais BRUTO 
    # aluno.nome = aluno.data.dict()['nome']
    # aluno.email = aluno.data.dict()['email']
    # aluno.faixa = aluno.data.dict()['faixa']
    # aluno.data_nascimento = aluno.data.dict()['data_nascimento']
    
    # modo mais Indicável
    # items -- separa em tuplas as chaves/valor
    for attr, value in aluno_data.dict().items():
        if value and attr != 'password': # <--- Importante ignorar o password aqui
            setattr(aluno, attr, value)

    aluno.save()
   
    return aluno


@treino_router.get('/meu_historico/', response= HistoricoCompletoSchema, auth=GlobalAuth())
def meu_historico(request):
    # O GlobalAuth já verificou o token e colocou o objeto User em request.auth
    usuario_logado = request.auth
    
    # 1. Buscando o Aluno que está vinculado a esse usuário logado
    try:
        aluno = Alunos.objects.get(usuario=usuario_logado)
    except Alunos.DoesNotExist:
        raise HttpError(404, "Perfil de aluno não encontrado.")

    # 1. Busca o histórico (detalhes)
    historico_qs = AulasConcluidas.objects.filter(aluno=aluno).order_by('-id')
    
    # 2. Cálculos de progresso (limpeza dos dados)
    aulas_feitas_na_faixa = historico_qs.filter(faixa_atual=aluno.faixa).count()
    
    label_faixa = aluno.get_faixa_display() 
    n = order_belt.get(label_faixa, 0)
    
    total_necessario = calculate_lesson_to_upgrade(n)
    faltam = max(0, total_necessario - aulas_feitas_na_faixa)

    # 3. Retorna o objeto combinado
    return {
        "nome": aluno.nome,
        "faixa_atual": label_faixa,
        "total_aulas_na_faixa": aulas_feitas_na_faixa,
        "aulas_faltantes": faltam,
        "detalhes": list(historico_qs) # Converte o queryset para lista para o schema
    }


 
    