- Enzo Pimentel Lorenzon — 14568409

## Requisitos

- **Python 3.12** ou superior
- **[uv](https://docs.astral.sh/uv/)** para gerenciar dependências e o ambiente virtual

```bash
pipx install uv
```

### Dependências

| Pacote | Versão testada |
| --- | --- |
| `fastapi[standard]` | 0.141.1 |
| `sqlalchemy` | 2.0.54 |

Não é preciso instalá-las à mão: o comando abaixo já as declara e o `uv` resolve
e baixa tudo na primeira execução. O banco é **SQLite**, que já vem embutido no
Python, então não precisa instalar mais nada.

## Como rodar

```bash
cd "Aula 3"
uv run --with "fastapi[standard]" --with sqlalchemy fastapi dev main.py
```

A aplicação vai subir em **http://127.0.0.1:8000/**. Utilize **http://127.0.0.1:8000/docs** para acessar o swagger dessa api.

O banco de dados (arquivo `cinema.db`) é criado automaticamente na primeira
execução, já com as tabelas. Para começar do zero, basta apagar ele.

### Alternativa sem uv

Quem preferir usar um ambiente virtual do Python com `pip`:

```bash
cd "Aula 3"
python3 -m venv .venv
source .venv/bin/activate      # no Windows: .venv\Scripts\activate
pip install "fastapi[standard]" sqlalchemy
fastapi dev main.py
```

## Endpoints criados
Todos os endpoints criados para essa aula estão listados abaixo.

### Filmes

| Método | URL | Funcionalidade |
| --- | --- | --- |
| `GET` | `/filmes` | Lista todos os filmes |
| `GET` | `/filmes/{codigo}` | Detalha um filme |
| `POST` | `/filmes` | Cadastra um filme |
| `PUT` | `/filmes/{codigo}` | Edita um filme |
| `DELETE` | `/filmes/{codigo}` | Remove um filme |

### Salas

| Método | URL | Funcionalidade |
| --- | --- | --- |
| `GET` | `/salas` | Lista todas as salas |
| `GET` | `/salas/{numero}` | Detalha uma sala |
| `POST` | `/salas` | Cadastra uma sala |
| `PUT` | `/salas/{numero}` | Edita uma sala |
| `DELETE` | `/salas/{numero}` | Remove uma sala |

### Sessões

| Método | URL | Funcionalidade |
| --- | --- | --- |
| `GET` | `/sessoes` | Lista todas as sessões |
| `GET` | `/sessoes?data=DD/MM/AAAA` | Lista as sessões de uma data |
| `GET` | `/sessoes/{codigo}` | Detalha uma sessão |
| `POST` | `/sessoes` | Cadastra uma sessão |
| `PUT` | `/sessoes/{codigo}` | Edita uma sessão |
| `DELETE` | `/sessoes/{codigo}` | Remove uma sessão |

### Tipos de ingresso

| Método | URL | Funcionalidade |
| --- | --- | --- |
| `GET` | `/tipos-ingresso` | Lista a tabela de preços |
| `GET` | `/tipos-ingresso/{tipo_sala}` | Detalha o preço de um tipo de sala |
| `POST` | `/tipos-ingresso` | Cadastra o valor do ingresso |
| `PUT` | `/tipos-ingresso/{tipo_sala}` | Edita o valor do ingresso |
| `DELETE` | `/tipos-ingresso/{tipo_sala}` | Remove o valor do ingresso |