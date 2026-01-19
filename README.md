<div align="center">
  <h1>🥋 Sistema de Gestão de Treinos e Graduação</h1>
  <p><i>API REST robusta para academias de Jiu-Jitsu e Artes Marciais</i></p>

  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django_Ninja-000000?style=for-the-badge&logo=fastapi&logoColor=white" alt="Django Ninja">
</div>

---

## 🚀 Sobre o Projeto
Este projeto foi desenvolvido para automatizar o controle de frequência e evolução de alunos. Ele utiliza **Django Ninja** para garantir uma API tipada, rápida e com documentação automática via Swagger.

## 👥 Níveis de Acesso e Permissões

### 🎖️ Instrutor (Staff)
O "Administrador" do sistema. Tem visão total sobre a academia:
* **Gestão Global:** Acesso à lista completa de alunos.
* **Controle de Presença:** Registro de aulas concluídas.
* **Graduação:** Autoridade para atualizar faixas e dados cadastrais.
* **Análise:** Consulta de métricas e progresso de qualquer aluno.

### 🥋 Aluno
Focado na experiência do usuário e transparência:
* **Painel Pessoal:** Visualização do resumo de progresso (Total vs Faltante).
* **Histórico:** Acesso restrito à sua própria lista de presenças.
* **Privacidade:** Dados protegidos por autenticação individual.

---

🔑 Configuração de Acesso (Staff)
Como o projeto utiliza autenticação via Token (Bearer), para testar as rotas do Staff, siga estes passos:

## Crie um Superusuário ##   
No terminal, execute o comando abaixo e siga as instruções para definir e-mail e senha:  
python manage.py createsuperuser 



## 🏗️ Estrutura da API (Principais Endpoints)

### 🔴 Área do Instrutor (Staff Required)

| Método | Endpoint | Descrição | Exemplo de JSON |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/login/` | Logar como staff. | </pre>{"email": "staff@email.com",  "senha": "123..."} </pre>|
| `GET` | `/api/aluno/` | Lista todos os alunos. | - |
| `POST` | `/api/aula_realizada/` | Registra presenças. |</pre> {"qtd": int,  "email_aluno": "jr@email.com"}</pre> |
| `GET` | `/api/progresso_aluno/` | Progresso do aluno. | </pre> api/progresso_aluno/?email_aluno=jr@email.com` </pre>|
| `PUT` | `/api/aluno/{id}/` | Atualiza dados/faixa. | </pre>{ "nome":"Melly","email":"jr@email.com","faixa": "M","data_nascimento": "2003-03-22"} </pre>|

### 🔵 Área do Aluno
| Método | Endpoint | Descrição | Exemplo de JSON |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/cadastro_aluno/` | Auto-cadastro inicial. | {"nome": "Junior", "email": "jr@email.com", "data_nascimento": "1988-03-22", "faixa" : "A","password" : "12345678 }
| `POST` | `/api/login/` | Obtém o token de acesso. | { "email": "jr@email.com", "senha": "12345678" }
| `GET` | `/api/meu_historico/` | Resumo e histórico pessoal. |

---

## 🛠️ Como Executar

### 1. Preparação
```bash
git clone [https://github.com/SEU_USUARIO/jiujitsuacademia.git](https://github.com/SEU_USUARIO/jiujitsuacademia.git)
pip install -r requirements.txt
python manage.py migrate
