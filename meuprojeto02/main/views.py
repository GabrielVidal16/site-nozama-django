import datetime
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

    
    if request.method == 'POST':
        form = LoginForm(request.POST)

        
        if form.is_valid():
           
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            
            bd = conecta_no_banco_de_dados()

            
            cursor = bd.cursor()
            cursor.execute("""
                        SELECT *
                        FROM usuarios
                        WHERE email = %s AND senha = %s;
                    """, (email, senha))
            usuario = cursor.fetchone()
            cursor.close()
            bd.close()

            
            if usuario:
                request.session['usuario_id'] = usuario[0]  # Salva o ID do usuário na sessão
                request.session['perfil'] = usuario[4]
                print(usuario[4])
                return redirect('home')  # Redireciona para a página inicial

            else:
                
                mensagem_erro = 'Email ou senha inválidos.'
                return render(request, 'login.html', {'form': form, 'mensagem_erro': mensagem_erro})

    else:
        
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('/login')

def registro(request):
    
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
         
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()

            sql = '''INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s,"usuario")'''

            
            cursor.execute(sql, (nome, email, senha))

            
            bd.commit()

            
            return redirect('login')  

    else:
        form = CadastroForm()

    return render(request, 'cadastro_usuario.html', {'form': form})
        
def home(request):
    products = []
    if not request.session.get('usuario_id'):
        return redirect('/login')
    
    usuario_id = request.session['usuario_id']

    
    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()
    
    
    cursor.execute('SELECT nome, perfil FROM usuarios WHERE usuario_id = %s;', (usuario_id,))
    usuario = cursor.fetchone()
    
    cursor.close()
    bd.close()

    if usuario:
        nome_usuario = usuario[0]  
        perfil = usuario[1]
        

    else:
        nome_usuario = 'Usuário não encontrado'

    try:
        
        con = conecta_no_banco_de_dados()
        cursor = con.cursor(dictionary=True)  
        cursor.execute('SELECT * FROM produtos')
        products = cursor.fetchall()  

    except mysql.connector.Error as error:
        print(f"Falha ao executar a consulta: {error}")
        return "Ocorreu um erro ao buscar os dados.", 500

    finally:
        if cursor:  
            cursor.close()
        if con and con.is_connected(): 
            con.close()
    

    return render(request, 'home.html', {'produtos': products, 'nome_usuario': nome_usuario, "perfil" : perfil})


def carrinho(request):
   
    itens = request.session.get('cart', {})

    
    total_carrinho = sum(item["preco"] * item["quantidade"] for item in itens.values())
    
    
    itens_renderizados = [
        {
            "nome": item["nome"],
            "preco": f"{item['preco']:.2f}",  
            "quantidade": item["quantidade"],
            "total": f"{item['preco'] * item['quantidade']:.2f}"  
        } for item in itens.values()
    ]
    
   
    total_carrinho_formatado = f"{total_carrinho:.2f}"
    contexto = {"itens": itens_renderizados, "total_carrinho": total_carrinho_formatado}
    
    return render(request, 'carrinho_de_compras.html', contexto)

def finalizar_compra(request):
    itens = request.session.get('cart', {})
    total_carrinho = sum(item["preco"] * item["quantidade"] for item in itens.values())
    itens_renderizados = [
        {
            "nome": item["nome"],
            "preco": f"{item['preco']:.2f}",  
            "quantidade": item["quantidade"],
            "total": f"{item['preco'] * item['quantidade']:.2f}" 
        } for item in itens.values()
    ]
    total_carrinho_formatado = f"{total_carrinho:.2f}"
    contexto = {"itens": itens_renderizados, "total_carrinho": total_carrinho_formatado}
    
    return render(request, 'compra_finalizada.html', contexto)

def compras(request):
    usuario_id = request.session['usuario_id']
    itens = request.session.get('cart', {})

    if not itens:
        return redirect('cart')  

    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()

    
    for item_id, item in itens.items():
        produto_id = item_id
        data_compra = datetime.datetime.now()

        sql = '''INSERT INTO usuario_compras (usuario_id, produto_id, data_compra)
                VALUES (%s, %s, %s)'''
        
        cursor.execute(sql, (usuario_id, produto_id, data_compra)) 

    
    bd.commit()
    cursor.close()
    bd.close()

    request.session['cart'] = {}

    return redirect('home')



def adicionar_ao_carrinho(request, produto_id):
    
    produtos = [
        {"produto_id": 1, "nome": "Elefante Psíquico de Guerra Pré-Histórico", "preco": 100.00, "imagem": "produto 1.jpeg"},
        {"produto_id": 2, "nome": "Lâmina do Caos", "preco": 150.00, "imagem": "produto 2.jpeg"},
        {"produto_id": 3, "nome": "Livro Misterioso", "preco": 200.00, "imagem": "produto 3.jpg"},
    ]

    
    produto = next((p for p in produtos if p["produto_id"] == produto_id), None)
    
    if not produto:
        return HttpResponse(status=404) 

    
    cart = request.session.get('cart', {})

    if produto_id in cart:
        cart[produto_id]["quantidade"] += 1
    else:
       
        cart[produto_id] = {
            "produto_id": produto["produto_id"],
            "nome": produto["nome"],
            "preco": produto["preco"],
            "quantidade": 1,
        }

 
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
            bd.commit() 
            cursor.close()
            bd.close()

            
            return redirect('home')     

        
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
            
            bd =conecta_no_banco_de_dados()
            cursor = bd.cursor()

            
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


