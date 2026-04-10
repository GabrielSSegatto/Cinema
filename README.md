# Cinema API

API REST para gerenciamento de um sistema de reservas de cinema. O sistema permite cadastrar salas, filmes e sessões, e possibilita que usuários realizem reservas de assentos com validação automática de conflitos, impedindo que um mesmo assento seja reservado duas vezes para a mesma sessão.

---

## Índice

- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Como Executar](#como-executar)
- [Endpoints da API](#endpoints-da-api)

---

## Tecnologias

- **Python 3** + **Flask 3.1**
- **SQLAlchemy** — ORM para comunicação com o banco de dados
- **Flask-Migrate** (Alembic) — versionamento e migrations do banco
- **SQLite** — banco de dados relacional em arquivo local
- **python-dotenv** — gerenciamento de variáveis de ambiente

---

## Arquitetura

O projeto segue uma arquitetura em camadas com separação clara de responsabilidades:

```
Cinema/
├── app.py          # Ponto de entrada — configura e inicializa a aplicação Flask
├── models.py       # Modelos do banco de dados (ORM via SQLAlchemy)
├── routes.py       # Endpoints HTTP — recebe requisições e delega para as services
├── services.py     # Lógica de negócio e validações
├── seed.py         # Script para popular o banco com dados iniciais
├── requirements.txt
└── .env            # Variáveis de ambiente (não versionado)
```

**Fluxo de uma requisição:**
```
Cliente HTTP → routes.py → services.py → models.py → Banco de dados
```

A camada de **routes** apenas valida os campos obrigatórios e delega o trabalho. Toda a lógica de negócio (validações, regras, conflitos) vive nas **services**.

---

### Entidades

| Entidade | Campos |
|---|---|
| `User` | `id`, `name`, `cpf` (único, 11 dígitos) |
| `Filme` | `id`, `titulo` |
| `Sala` | `id`, `nome`, `tipo` (2D/3D/IMAX), `capacidade` |
| `Sessao` | `id`, `horario_data`, `is_dub`, `filme_id`, `sala_id` |
| `Assento` | `id`, `numero`, `sala_id` |
| `Reserva` | `id`, `user_id`, `sessao_id`, `assento_id`, `data_reserva` |

### Regras de integridade

- **Conflito de reserva**: o sistema bloqueia automaticamente reservas duplicadas para o mesmo assento na mesma sessão.
- **CPF único**: não é possível cadastrar dois usuários com o mesmo CPF.
- **Delete em cascata**: ao deletar uma `Sala`, todas as suas sessões e assentos são removidos. Ao deletar um `User`, suas reservas são removidas junto.

---

## Como Executar

### 1. Clone o repositório e entre na pasta

```bash
git clone https://github.com/GabrielSSegatto/Cinema
cd Cinema
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
DATABASE_URL=sqlite:///cinema.db
SECRET_KEY=sua_chave_secreta_aqui
FLASK_APP=app.py
FLASK_DEBUG=True
```

### 5. Execute as migrations

```bash
flask db upgrade
```

> Isso cria o banco de dados `cinema.db` com todas as tabelas.

### 6. (Opcional) Popule o banco com dados de exemplo

```bash
python seed.py
```

Isso cria 2 salas, 2 filmes, 2 sessões, 20 assentos, 2 usuários e 1 reserva inicial para facilitar os testes.

### 7. Inicie o servidor

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`.

---

## Endpoints da API

Todos os endpoints retornam e recebem JSON. Os códigos de status seguem o padrão REST:
- `200` — OK
- `201` — Criado com sucesso
- `400` — Erro de validação
- `404` — Recurso não encontrado
- `500` — Erro interno

---

### Usuários — `/users`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/users` | Lista todos os usuários |
| `GET` | `/users/<id>` | Retorna um usuário pelo ID |
| `POST` | `/users` | Cria um novo usuário |
| `PUT` | `/users/<id>` | Atualiza um usuário |
| `DELETE` | `/users/<id>` | Remove o usuário e suas reservas |

**POST /users** — corpo da requisição:
```json
{
  "name": "João Gabriel",
  "cpf": "12345678901"
}
```

---

### Filmes — `/filmes`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/filmes` | Lista todos os filmes |
| `GET` | `/filmes/<id>` | Retorna um filme pelo ID |
| `POST` | `/filmes` | Cadastra um novo filme |
| `PUT` | `/filmes/<id>` | Atualiza um filme |
| `DELETE` | `/filmes/<id>` | Remove o filme e suas sessões |

**POST /filmes** — corpo da requisição:
```json
{
  "titulo": "Matrix"
}
```

---

### Salas — `/salas`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/salas` | Lista todas as salas |
| `GET` | `/salas/<id>` | Retorna uma sala pelo ID |
| `POST` | `/salas` | Cria uma nova sala |
| `PUT` | `/salas/<id>` | Atualiza uma sala |
| `DELETE` | `/salas/<id>` | Remove a sala, seus assentos e sessões |

**POST /salas** — corpo da requisição:
```json
{
  "nome": "Sala 01",
  "tipo": "IMAX",
  "capacidade": 100
}
```

---

### Assentos — `/assentos`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/assentos` | Lista todos os assentos |
| `GET` | `/assentos/<id>` | Retorna um assento pelo ID |
| `POST` | `/assentos` | Cria um novo assento |
| `PUT` | `/assentos/<id>` | Atualiza um assento |
| `DELETE` | `/assentos/<id>` | Remove o assento e suas reservas |

**POST /assentos** — corpo da requisição:
```json
{
  "numero": "A1",
  "sala_id": 1
}
```

---

### Sessões — `/sessoes`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/sessoes` | Lista todas as sessões |
| `GET` | `/sessoes/<id>` | Retorna uma sessão pelo ID |
| `POST` | `/sessoes` | Cria uma nova sessão |
| `PUT` | `/sessoes/<id>` | Atualiza uma sessão |
| `DELETE` | `/sessoes/<id>` | Remove a sessão e suas reservas |

**POST /sessoes** — corpo da requisição:
```json
{
  "horario_data": "2025-12-01T20:00:00",
  "is_dub": false,
  "filme_id": 1,
  "sala_id": 1
}
```

> `is_dub`: `true` para dublado, `false` para legendado.

---

### Reservas — `/reservas`

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/reservas` | Lista todas as reservas |
| `GET` | `/reservas/<id>` | Retorna uma reserva pelo ID |
| `POST` | `/reservas` | Cria uma nova reserva |
| `PUT` | `/reservas/<id>` | Atualiza uma reserva |
| `DELETE` | `/reservas/<id>` | Remove uma reserva |

**POST /reservas** — corpo da requisição:
```json
{
  "user_id": 1,
  "sessao_id": 1,
  "assento_id": 1
}
```

> ⚠️ Se o assento já estiver reservado para aquela sessão, a API retorna `400` com a mensagem `"Este assento já está reservado para esta sessão"`.
