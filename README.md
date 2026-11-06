# Nozama

Loja virtual feita com Django.

## Executando localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
cd meuprojeto02
python manage.py migrate
python manage.py runserver
```

O projeto usa SQLite por padrão. Para usar MySQL, configure as variáveis `DB_*`
do arquivo `.env.example` e instale o driver correspondente.

## Estrutura

- `meuprojeto02/main`: catálogo, autenticação, carrinho e compras.
- `meuprojeto02/meuprojeto02`: configurações e rotas do projeto.
- `meuprojeto02/main/templates`: páginas HTML.
- `meuprojeto02/main/static`: estilos e arquivos estáticos.
