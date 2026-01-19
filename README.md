## 🥋 Sistema de Gestão de Treinos e Graduação (BJJ/Artes Marciais) ##
Esta é uma API REST robusta desenvolvida com Django Ninja (API Fast & Type-Safe com Pydantic) para gerir o progresso de alunos em academias de artes marciais.   
O sistema controla desde o cadastro e autenticação até o histórico de aulas e a contagem automatizada para a próxima faixa.

🚀 Funcionalidades
🔐 Autenticação e Níveis de Acesso
Sistema de Login: Autenticação baseada em Tokens (Bearer Token).

Instrutor (Staff): Possui permissão para listar todos os alunos, atualizar dados, e marcar aulas realizadas e ver progresso  
Aluno: Acesso restrito ao seu próprio histórico de aulas

📈 Gestão de Alunos & Progresso
Cadastro Automatizado: Criação simultânea de usuário do Django (User) e perfil do aluno (Alunos).

Regra de Negócio de Graduação: Validação de idade para faixas avançadas e cálculo dinâmico de aulas faltantes para a próxima promoção.
Histórico Detalhado: Dashboard para o aluno visualizar o total de aulas na faixa atual e a lista de presenças.  
Autorização: * No Postman ou Insomnia, utilize esse token como um Bearer Token no cabeçalho das requisições para as rotas abaixo.


🔑 Configuração de Acesso (Staff)
Como o projeto utiliza autenticação via Token (Bearer), para testar as rotas de Instrutor, siga estes passos:

##Crie um Superusuário##   
No terminal, execute o comando abaixo e siga as instruções para definir e-mail e senha:  
python manage.py createsuperuser  
Utilize o endpoint POST /api/login/ enviando o e-mail e senha que você acabou de criar.

A API retornará um campo "token".

🏗️ Estrutura do Projeto (Endpoints Principais)  
Instrutor (Necessário is_staff=True)<br>  
MétodoEndpointDescrição<br>
POST ----   /api/login/  
{
    "email": "staff@email.com",
    "senha": "12345678"
}
GET  ----  /api/aluno/----------------Lista todos os alunos cadastrados.  
POST ----  /api/aula_realizada/-------Registra presenças para um aluno específico.  
{  
    "qtd": int,  
    "email_aluno": "email@email.com"
  
}  
GET  ----  /api/progresso_aluno/?email_aluno=email@email.com------Consulta detalhada do progresso de qualquer aluno.  
PUT  ----  /api/aluno/{id}/-----------Atualiza dados cadastrais e faixa.  
{
  
        "nome": "Melly",
        "email": "melly@email.com",
        "faixa": "M",
        "data_nascimento": "2003-03-22"
 
}

