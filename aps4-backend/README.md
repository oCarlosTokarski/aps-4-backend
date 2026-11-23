# Aps 4 Back - End Unisenai

## Feito por:
Carlos Tokarski Borges Neto <br>
Dheyvid Bastos Pinto

## API de Eventos Acadêmicos

## API RESTful desenvolvida em Python utilizando FastAPI para gerenciamento de eventos acadêmicos, participantes e inscrições.

# 🛠️ Tecnologias

Python

FastAPI

Pydantic

SQLite

SQLAlchemy ORM

PyJWT (tokens JWT)

pwdlib com Argon2 (hash de senhas)

python-dotenv (variáveis de ambiente)

Uvicorn

# 📦 Instalação

Clone ou baixe o projeto e entre na pasta.

Instale as dependências:

pip install -r requirements.txt

# 🔑 Configuração da chave secreta (.env)

crie um arquivo .env com esse codigo abaixo:
# Gere uma com: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=troque-por-uma-chave-gerada


TOKEN_EXPIRACAO_MINUTOS=30


ADMIN_NOME=Administrador <br>
ADMIN_EMAIL=admin@exemplo.com<br>
ADMIN_SENHA=12345678


A chave usada para assinar os tokens JWT **não fica no código**. Ela é lida do arquivo `.env`.

1. Copie o arquivo de exemplo:

```
cp .env.example .env
```

(no Windows: `copy .env.example .env`)

2. Gere uma chave e coloque no campo `SECRET_KEY` do `.env`:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

3. Preencha também `ADMIN_EMAIL` e `ADMIN_SENHA` (administrador inicial, com senha de pelo menos 8 caracteres).

O arquivo `.env` está no `.gitignore` e não deve ser enviado ao GitHub.
Sem a `SECRET_KEY` a aplicação não inicia.

Variáveis do `.env`:

- `SECRET_KEY`: chave de assinatura dos tokens (obrigatória)
- `TOKEN_EXPIRACAO_MINUTOS`: validade do token (padrão 30)
- `ADMIN_NOME`, `ADMIN_EMAIL`, `ADMIN_SENHA`: administrador criado automaticamente ao iniciar a API

# ▶️ Executando o projeto

Execute o seguinte comando:

uvicorn main:app --reload

# 📚 Swagger

A documentação da API é disponibilizada automaticamente pelo FastAPI.

Após iniciar o projeto, acesse:

http://127.0.0.1:8000/docs


No Swagger é possível visualizar e testar todas as rotas da API.

# 📌 Funcionalidades
## 📅 Eventos

Cadastrar evento

Listar eventos

Consultar evento

Atualizar evento

Excluir evento

# 👤 Participantes

Cadastrar participante

Listar participantes

Consultar participante

Atualizar participante

Excluir participante

# 📝 Inscrições

Inscrever participante em evento

Consultar participantes inscritos

Verificar disponibilidade de vagas

Impedir inscrições duplicadas

# ✅ Validações

A API possui validações para os dados enviados, como:

Campos obrigatórios

E-mail válido

Capacidade maior que zero

Data válida

Campos de texto não vazios (texto só com espaços também é recusado)

# ⚠️ Tratamento de erros

A API trata situações como:

Evento não encontrado

Participante não encontrado

Participante já inscrito

Evento sem vagas

Dados inválidos

# 📁 Estrutura do projeto

O projeto utiliza uma separação baseada em MVC:

controller — responsável pelas rotas da API

model — entidades do banco de dados e seus relacionamentos (SQLAlchemy)

schema — validação dos dados de entrada e saída (Pydantic)

service — responsável pelas regras de negócio e consultas ao banco

database.py — conexão com o SQLite, sessões e criação das tabelas

security — hash de senhas (Argon2), geração/validação de tokens JWT e dependências que protegem as rotas

main.py — responsável pela inicialização da aplicação

```
projeto/
├── main.py
├── database.py
├── controller/   (evento, participante, inscricao, relatorio, usuario, auth)
├── model/        (evento, participante, inscricao, usuario)
├── schema/       (evento, participante, inscricao, relatorio, usuario)
├── service/      (evento, participante, inscricao, relatorio, usuario, auth)
└── security/     (security.py: hash de senha, JWT e dependências de acesso)
```

# 💾 Armazenamento (Banco de dados)

Os dados são persistidos em um banco **SQLite** acessado com **SQLAlchemy ORM**.

O arquivo do banco é o `eventos.db`, criado automaticamente na raiz do projeto
na primeira execução (as tabelas também são criadas automaticamente em `main.py`).
Os dados continuam disponíveis após reiniciar a aplicação.
Para zerar os dados, basta apagar o arquivo `eventos.db`.

Tabelas:

- eventos (id, titulo, descricao, data, horario, local, capacidade, categoria)
- participantes (id, nome, email único, curso)
- inscricoes (id, evento_id, participante_id, data_inscricao) — com restrição
  de unicidade em (evento_id, participante_id)

Ao excluir um evento ou participante, as inscrições relacionadas também são
excluídas (cascade), evitando registros órfãos.
Não é permitido reduzir a capacidade de um evento abaixo do número de inscritos (409).

# 🛣️ Principais rotas

Acesso: **Público** = sem token; **Logado** = qualquer usuário autenticado; **Admin** = somente administrador.

| Método | Rota | Descrição | Acesso |
|--------|------|-----------|--------|
| POST | /usuarios | Cadastrar usuário (perfil sempre `usuario`) | Público |
| POST | /auth/login | Login (retorna o token JWT) | Público |
| GET | /auth/me | Dados do usuário autenticado | Logado |
| GET | /eventos | Listar eventos | Público |
| GET | /eventos/{id} | Consultar evento | Público |
| POST | /eventos | Cadastrar evento | Admin |
| PUT | /eventos/{id} | Atualizar evento | Admin |
| DELETE | /eventos/{id} | Excluir evento | Admin |
| POST | /participantes | Cadastrar participante | Logado |
| GET | /participantes | Listar participantes | Logado |
| GET | /participantes/{id} | Consultar participante | Logado |
| PUT | /participantes/{id} | Atualizar participante | Admin |
| DELETE | /participantes/{id} | Excluir participante | Admin |
| POST | /eventos/{evento_id}/inscricoes/{participante_id} | Inscrever participante | Logado |
| GET | /eventos/{evento_id}/inscricoes | Listar inscritos do evento | Admin |
| GET | /relatorios/eventos/ocupacao | Relatório de ocupação | Admin |
| GET | /relatorios/eventos/categorias | Relatório por categoria | Admin |
| GET | /relatorios/participantes/cursos | Relatório por curso | Admin |

Códigos de erro principais: 401 (sem token, token inválido/expirado ou login errado),
403 (sem permissão), 404 (não encontrado), 409 (e-mail já cadastrado, inscrição duplicada,
evento sem vagas), 422 (dados inválidos).

# 👥 Perfis e permissões

- **usuario** (padrão de quem se cadastra em `POST /usuarios`): consulta eventos, cadastra e consulta
  participantes, realiza inscrições e consulta seus dados em `/auth/me`.
- **administrador**: tudo que o usuário faz, mais cadastrar/atualizar/excluir eventos, atualizar/excluir
  participantes, listar inscritos de um evento e consultar os relatórios.

O perfil nunca é informado pelo cliente: se o corpo do `POST /usuarios` contiver o campo `perfil`,
a API recusa a requisição (422). O primeiro administrador é criado automaticamente ao iniciar a API
com os dados `ADMIN_EMAIL` e `ADMIN_SENHA` do `.env`. As permissões são verificadas no servidor
a cada requisição, usando o perfil gravado no banco (e não algo enviado pelo cliente).

# 🔐 Segurança

- Senhas guardadas apenas como **hash Argon2** (biblioteca `pwdlib`). A senha original e o hash nunca são retornados.
- Senha com no mínimo 8 caracteres.
- Token **JWT** (PyJWT, algoritmo HS256) com o id do usuário (`sub`) e validade (`exp`, padrão 30 min).
- O token é enviado no cabeçalho `Authorization: Bearer <token>`.
- Tokens ausentes, inválidos, adulterados ou expirados retornam 401.
- Login com e-mail ou senha errados retorna 401 com a mesma mensagem nos dois casos.

# 🔑 Como cadastrar usuário e obter o token

1. Cadastre um usuário comum (`POST /usuarios`):

```json
{
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "senha": "senha_segura"
}
```

Resposta (201):

```json
{
  "id": 2,
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "perfil": "usuario"
}
```

2. Faça login (`POST /auth/login`):

```json
{
  "email": "aluno@exemplo.com",
  "senha": "senha_segura"
}
```

Resposta (200):

```json
{
  "access_token": "token_jwt_gerado",
  "token_type": "bearer"
}
```

3. No Swagger (`/docs`), clique em **Authorize**, cole apenas o valor do `access_token` e confirme.
   Fora do Swagger, envie o cabeçalho `Authorization: Bearer token_jwt_gerado`.

Para usar rotas de administrador, faça login com o e-mail e a senha definidos em `ADMIN_EMAIL` e `ADMIN_SENHA`.

Erros de exemplo:

```json
{ "detail": "E-mail ou senha inválidos." }
{ "detail": "Não foi possível validar as credenciais." }
{ "detail": "Você não possui permissão para executar esta operação." }
{ "detail": "Já existe um usuário cadastrado com este e-mail." }
```

# 📊 Relatórios

Todos são calculados dinamicamente com consultas SQLAlchemy (JOIN, GROUP BY, COUNT e SUM).

**Ocupação dos eventos** — `GET /relatorios/eventos/ocupacao`
Para cada evento: capacidade, total de inscritos, vagas disponíveis e percentual de ocupação (inclui eventos sem inscrições).

```json
[
  {
    "evento_id": 1,
    "titulo": "Workshop de Python",
    "capacidade": 40,
    "total_inscritos": 10,
    "vagas_disponiveis": 30,
    "percentual_ocupacao": 25.0
  }
]
```

**Eventos por categoria** — `GET /relatorios/eventos/categorias`
Por categoria: total de eventos, capacidade total e total de inscrições.

```json
[
  {
    "categoria": "Workshop",
    "total_eventos": 3,
    "capacidade_total": 120,
    "total_inscricoes": 95
  }
]
```

**Participação por curso** — `GET /relatorios/participantes/cursos`
Por curso: total de participantes cadastrados (sem repetir) e total de inscrições.

```json
[
  {
    "curso": "Engenharia de Software",
    "total_participantes": 80,
    "total_inscricoes": 150
  }
]
```

Se não houver registros, os relatórios retornam uma lista vazia (`[]`).

# 💡 Exemplos de utilização

Cadastrar participante (`POST /participantes`):

```json
{
  "nome": "Maria Silva",
  "email": "maria@email.com",
  "curso": "Engenharia de Software"
}
```

Cadastrar evento (`POST /eventos`):

```json
{
  "titulo": "Workshop de Python",
  "descricao": "Introdução à linguagem",
  "data": "2026-12-10",
  "horario": "19:00:00",
  "local": "Laboratório 3",
  "capacidade": 40,
  "categoria": "Workshop"
}
```

Inscrever (`POST /eventos/1/inscricoes/1`), resposta 201:

```json
{
  "id": 1,
  "evento_id": 1,
  "participante_id": 1,
  "data_inscricao": "2026-11-23"
}
```

Inscrição duplicada (409):

```json
{ "detail": "Participante já está inscrito neste evento." }
```

# 🧪 Como reproduzir os testes

1. Configure o `.env`, inicie a API com `uvicorn main:app --reload` e abra `http://127.0.0.1:8000/docs`.
2. **Usuário:** cadastre um usuário (201), tente cadastrar o mesmo e-mail de novo (409) e tente enviar o campo `perfil` (422).
3. **Hash:** abra o arquivo `eventos.db` (ex.: DB Browser for SQLite) e veja que a coluna `senha_hash` guarda o hash, nunca a senha.
4. **Login:** faça login com dados corretos (200 + token) e com dados errados (401).
5. **Sem token:** chame `POST /eventos` ou `GET /relatorios/eventos/ocupacao` sem token (401).
6. **Token inválido:** use um token alterado em **Authorize** (401). Para testar expiração, coloque `TOKEN_EXPIRACAO_MINUTOS=1` no `.env`, reinicie, faça login e tente usar o token após 1 minuto (401).
7. **Token válido:** com o token do usuário, chame `GET /auth/me` (200) e faça uma inscrição (201).
8. **Permissão:** com o token do usuário comum, tente `POST /eventos` (403). Com o token do administrador, o mesmo cadastro funciona (201).
9. **APS 3:** com o administrador, cadastre eventos e participantes, faça inscrições e consulte os 3 relatórios, alterando e excluindo registros para ver os valores mudarem.
10. Pare o servidor, inicie novamente e confira que os dados continuam salvos.
