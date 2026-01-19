from django.db import models
from django.contrib.auth.models import User

faixa_choice = (
        ('B', 'Branca'),
        ('A', 'Azul'),
        ('R', 'Roxa'),
        ('M', 'Marrom'),
        ('P', 'Preta')
    )

class Alunos(models.Model):
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField(null=True, blank=True)
    faixa = models.CharField(max_length=1, choices=faixa_choice, default='B')

    def __str__(self):
        return self.nome
    
class AulasConcluidas(models.Model):

    aluno = models.ForeignKey(Alunos, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    faixa_atual = models.CharField(max_length=1, choices=faixa_choice, default='B')

    def __str__(self):
        return self.aluno.nome
    



