from django.http import HttpResponseRedirect  # Usado para redirecionar o usuário para uma nova URL
from django.shortcuts import render, redirect
import mysql  # 'render' para renderizar templates e 'redirect' para redirecionar o usuário
from main.bd_config import conecta_no_banco_de_dados  # Função personalizada para conectar-se ao banco de dados
from .forms import ContatoForm, LoginForm  # Importa o formulário personalizado 'ContatoForm' para manipulação de dados do usuário
from .forms import CadastroForm
from .models import Usuario
from django.shortcuts import render  # Usado para renderizar templates HTML com dados contextuais
from django.contrib.auth import authenticate, login  # Funções de autenticação para autenticar, logar e deslogar usuários
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User  # Modelo de usuário padrão do Django, para criação e manipulação de usuários
#from django.contrib.auth.decorators import login_required  # Para proteger views que exigem um usuário autenticado (comentado)
from django.views.decorators.csrf import csrf_protect  # Ativa a proteção CSRF para uma view específica
from django.contrib.auth.decorators import login_required  # Decorator que exige que o usuário esteja autenticado para acessar a view
from django.contrib.auth.mixins import LoginRequiredMixin  # Mixin para garantir que apenas usuários autenticados acessem views baseadas em classe
from django.shortcuts import render, redirect  # 'render' para templates e 'redirect' para redirecionamentos de URL
from django.http import HttpResponseBadRequest  # Retorna uma resposta HTTP com erro 400 (Bad Request)
from django.db import transaction  # Usado para controlar transações de banco de dados (commit/rollback)
from django.http import HttpResponse, JsonResponse  # 'HttpResponse' para resposta genérica e 'JsonResponse' para respostas JSON
from django.contrib import messages  # Usado para mostrar mensagens de feedback ao usuário, como sucesso ou erro
itens = {}

def login(request):
    request.session['usuario_id'] = ""

    # Se for uma solicitação POST, valida o login
    if request.method == 'POST':
        form = LoginForm(request.POST)

        # Verifique se o formulário foi validado corretamente
        if form.is_valid():
            # Extrair as credenciais do formulário
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Conectar ao banco de dados
            bd = conecta_no_banco_de_dados()

            # Verificar as credenciais no banco de dados
            cursor = bd.cursor()
            cursor.execute("""
                        SELECT *
                        FROM usuarios
                        WHERE email = %s AND senha = %s;
                    """, (email, senha))
            usuario = cursor.fetchone()
            cursor.close()
            bd.close()

            # Se o usuário for encontrado
            if usuario:
                request.session['usuario_id'] = usuario[0]  # Salva o ID do usuário na sessão
                request.session['perfil'] = usuario[4]
                print(usuario[4])
                return redirect('home')  # Redireciona para a página inicial

            else:
                # Se não encontrar o usuário, exibe uma mensagem de erro
                mensagem_erro = 'Email ou senha inválidos.'
                return render(request, 'login.html', {'form': form, 'mensagem_erro': mensagem_erro})

    else:
        # Caso contrário, cria um formulário vazio
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('/login')

def registro(request):
    
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            # Extrair os dados do formulário
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            # Conectar ao banco de dados (usando Django ORM)
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()

            sql = '''INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s,"usuario")'''

            # Executar o comando com os valores
            cursor.execute(sql, (nome, email, senha))

            # Confirmar a transação
            bd.commit()

            # Salva o ID do usuário na sessão
            return redirect('login')  # Redireciona para a página inicial

    else:
        form = CadastroForm()

    return render(request, 'cadastro_usuario.html', {'form': form})
        
def home(request):
    products = []
    if not request.session.get('usuario_id'):
        return redirect('/login')
    
    usuario_id = request.session['usuario_id']

    # Conecte-se ao banco de dados e recupere o nome do usuário
    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()
    
    # Execute a consulta para buscar o nome do usuário
    cursor.execute('SELECT nome, perfil FROM usuarios WHERE usuario_id = %s;', (usuario_id,))
    usuario = cursor.fetchone()
    
    cursor.close()
    bd.close()

    if usuario:
        nome_usuario = usuario[0]  # Assumindo que "nome" está na primeira posição
        perfil = usuario[1]
        

    else:
        nome_usuario = 'Usuário não encontrado'

    try:
        # Conectando ao banco de dados
        con = conecta_no_banco_de_dados()
        cursor = con.cursor(dictionary=True)  # Use dictionary=True para retornar resultados como dicionários
        cursor.execute('SELECT * FROM produtos')
        products = cursor.fetchall()  # Use fetchall() para obter todos os registros

    except mysql.connector.Error as error:
        print(f"Falha ao executar a consulta: {error}")
        return "Ocorreu um erro ao buscar os dados.", 500

    finally:
        if cursor:  # Verifica se o cursor foi inicializado
            cursor.close()
        if con and con.is_connected():  # Verifica se a conexão foi estabelecida e está aberta
            con.close()
    

    return render(request, 'home.html', {'produtos': products, 'nome_usuario': nome_usuario, "perfil" : perfil})


def carrinho(request):
    # Recupera o carrinho da sessão, ou inicializa um carrinho vazio
    itens = request.session.get('cart', {})

    # Calcula o total do carrinho
    total_carrinho = sum(item["preco"] * item["quantidade"] for item in itens.values())
    
    # Prepara os dados para renderizar no template
    itens_renderizados = [
        {
            "nome": item["nome"],
            "preco": f"{item['preco']:.2f}",  # Formata o preço unitário
            "quantidade": item["quantidade"],
            "total": f"{item['preco'] * item['quantidade']:.2f}"  # Formata o total por produto
        } for item in itens.values()
    ]
    
    # Formata o total geral
    total_carrinho_formatado = f"{total_carrinho:.2f}"
    contexto = {"itens": itens_renderizados, "total_carrinho": total_carrinho_formatado}
    
    return render(request, 'carrinho_de_compras.html', contexto)

def adicionar_ao_carrinho(request, produto_id):
    # Lista de produtos disponíveis
    produtos = [
        {"produto_id": 1, "nome": "Elefante Psíquico de Guerra Pré-Histórico", "preco": 100.00, "imagem": "produto 1.jpeg"},
        {"produto_id": 2, "nome": "Lâmina do Caos", "preco": 150.00, "imagem": "produto 2.jpeg"},
        {"produto_id": 3, "nome": "Livro Misterioso", "preco": 200.00, "imagem": "produto 3.jpg"},
    ]

    # Encontrar o produto com o ID correspondente
    produto = next((p for p in produtos if p["produto_id"] == produto_id), None)
    
    if not produto:
        return HttpResponse(status=404)  # Produto não encontrado

    # Recupera o carrinho da sessão, ou inicializa um carrinho vazio
    cart = request.session.get('cart', {})

    # Se o produto já está no carrinho, incrementa a quantidade
    if produto_id in cart:
        cart[produto_id]["quantidade"] += 1
    else:
        # Adiciona o produto ao carrinho com quantidade inicial de 1
        cart[produto_id] = {
            "produto_id": produto["produto_id"],
            "nome": produto["nome"],
            "preco": produto["preco"],
            "quantidade": 1,
        }

    # Salva o carrinho atualizado na sessão
    request.session['cart'] = cart
    
    return HttpResponse(status=204)

    

def editarproduto(request,id):
    if not request.session.get('usuario_id'):
        return redirect('/login')
    else:
        produto_id = id
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute("""
            SELECT produto_id, nome, preco
            FROM produtos
            WHERE produto_id = %s;
        """, (id,))
        dados_produto = cursor.fetchone()
        cursor.close()
        bd.close()
        if request.method == 'POST':
            nome = request.POST.get('nome')
            preco = request.POST.get('preco')    
            if not all([nome, preco]):
                return render(request, 'produtos.html')
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            sql = (
                """
                UPDATE produtos
                SET nome = %s, preco = %s
                WHERE produto_id = %s;
                """
            )
            values = (nome, preco,produto_id)
            cursor.execute(sql, values)
            bd.commit()  # Assumindo que você tenha gerenciamento de transações
            cursor.close()
            bd.close()

            # Redirecione para a página de sucesso ou exiba a mensagem de confirmação
            return redirect('home')     

        # Exiba o formulário (assumindo lógica de renderização)
        return render(request, 'editarproduto.html',{'id': produto_id})

def produtos(request):
    if not request.session.get('usuario_id'):
            return redirect('/login')
    

    usuario_id = request.session['usuario_id']

    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()
    
    cursor.execute('SELECT perfil FROM usuarios WHERE usuario_id = %s;', (usuario_id,))
    usuario = cursor.fetchone()
    
    cursor.close()
    bd.close()

    if usuario:
        perfil = usuario[0]
        
    print(perfil)
    if perfil == 'usuario':
        return redirect('home')

    else:
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute('SELECT * FROM produtos;')
        produtos = cursor.fetchall()

        return render(request, 'produtos.html', {"produtos": produtos})

def excluirproduto(request,id):
    produto_id = id
    if not request.session.get('usuario_id'):
            return redirect('/login')
    else:
        try:
            # Estabelecer conexão com o banco de dados (substitua 'seu_banco_de_dados' pelo nome real)
            bd =conecta_no_banco_de_dados()
            cursor = bd.cursor()

            # Evitar SQL injection usando parâmetros nomeados
            sql = (
                """
                DELETE FROM produtos WHERE produto_id = %s;
                """
            )
            values = (produto_id,)
            cursor.execute(sql, values)
            bd.commit()
            cursor.close()

            messages.success(request, 'produto excluído com sucesso!')
            return redirect('produtos')

        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            messages.error(request, 'Falha ao excluir produto. Tente novamente mais tarde.')
            return redirect('produtos')


