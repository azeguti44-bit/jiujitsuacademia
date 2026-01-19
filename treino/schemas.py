from ninja import ModelSchema, Schema
from .models import Alunos
from typing import Optional
from pydantic import Field, field_validator
from datetime import date
from typing import List



# Use este para DEVOLVER os dados para o Postman (sem senha por segurança!)
class AlunoOutSchema(ModelSchema):
    class Meta:
        model = Alunos
        fields = ['id', 'nome', 'email', 'faixa', 'data_nascimento']


# RECEBER os dados do Postman (com senha)
class AlunoInSchema(Schema):
    nome: str
    email: str
    faixa: str
    data_nascimento: date
    password: str


# O Schema cria a partir de uma ModelSchema
class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa: str
    total_aulas: int
    aulas_necessarias_para_proxima_faixa: int


class AulaRealizadaSchema(Schema):
    qtd: Optional[int]=1
    email_aluno: str


class HistoricoAulasSchema(Schema):
    id: int
    faixa_atual: str
    data: date 

class LoginSchema(Schema):
    email: str
    senha: str

class AlunoUpdateSchema(Schema):
    nome: str
    email: str
    faixa: str
    data_nascimento: date

class HistoricoCompletoSchema(Schema):
    nome: str
    faixa_atual: str
    total_aulas_na_faixa: int
    aulas_faltantes: int
    detalhes: List[HistoricoAulasSchema]