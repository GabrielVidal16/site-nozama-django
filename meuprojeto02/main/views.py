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

            sql = '''INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)'''

            # Executar o comando com os valores
            cursor.execute(sql, (nome, email, senha))

            # Confirmar a transação
            bd.commit()

            # Salva o ID do usuário na sessão
            return redirect('login')  # Redireciona para a página inicial

    else:
        form = CadastroForm()

    return render(request, 'cadastro_usuario.html', {'form': form})

def paginainicial(request):
        if not request.session.get('usuario_id'):
            return redirect('/')
        else:

            # Obtenha o ID do usuário armazenado na sessão
            usuario_id = request.session['usuario_id']

            # Conecte-se ao banco de dados e recupere o nome do usuário
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            
            # Execute a consulta para buscar o nome do usuário
            cursor.execute('SELECT nome FROM usuarios WHERE usuario_id = %s;', (usuario_id,))
            usuario = cursor.fetchone()
            
            cursor.close()
            bd.close()

            if usuario:
                nome_usuario = usuario[0]  # Assumindo que "nome" está na primeira posição
            else:
                nome_usuario = 'Usuário não encontrado'

            # Passe o nome do usuário para o template
            return render(request, 'paginainicial.html', {'nome_usuario': nome_usuario})
        
def home(request):
    products = []
    if not request.session.get('usuario_id'):
        return redirect('/login')
    
    usuario_id = request.session['usuario_id']
    print(usuario_id)

    # Conecte-se ao banco de dados e recupere o nome do usuário
    bd = conecta_no_banco_de_dados()
    cursor = bd.cursor()
    
    # Execute a consulta para buscar o nome do usuário
    cursor.execute('SELECT nome FROM usuarios WHERE usuario_id = %s;', (usuario_id,))
    usuario = cursor.fetchone()
    
    cursor.close()
    bd.close()

    if usuario:
        nome_usuario = usuario[0]  # Assumindo que "nome" está na primeira posição
    else:
        nome_usuario = 'Usuário não encontrado'

    try:
        # Conectando ao banco de dados
        con = conecta_no_banco_de_dados()
        cursor = con.cursor(dictionary=True)  # Use dictionary=True para retornar resultados como dicionários
        cursor.execute('SELECT * FROM produtos')
        products = cursor.fetchall()  # Use fetchall() para obter todos os registros
        print(f"estes sao os produtos{products}")

    except mysql.connector.Error as error:
        print(f"Falha ao executar a consulta: {error}")
        return "Ocorreu um erro ao buscar os dados.", 500

    finally:
        if cursor:  # Verifica se o cursor foi inicializado
            cursor.close()
        if con and con.is_connected():  # Verifica se a conexão foi estabelecida e está aberta
            con.close()
    

    return render(request, 'home.html', {'produtos': products, 'nome_usuario': nome_usuario})


def carrinho(request):
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
    

def adicionar_ao_carrinho(request,produto_id):
    
    
    # Lista de produtos disponíveis
    produtos = [
        {"produto_id": 1, "nome": "Elefante Psíquico de Guerra Pré-Histórico", "preco": 100.00, "imagem": "produto 1.jpeg"},
        {"produto_id": 2, "nome": "Lâmina do Caos", "preco": 150.00, "imagem": "produto 2.jpeg"},
        {"produto_id": 3, "nome": "Livro Misterioso", "preco": 200.00, "imagem": "produto 3.jpg"},
    ]

    # Encontrar o produto com o ID correspondente
    produto = next((p for p in produtos if p["produto_id"] == produto_id), None)

    if produto:
        # Se o produto já está no carrinho, incrementa a quantidade
        if produto_id in itens:
            itens[produto_id]["quantidade"] += 1
        else:
            # Adiciona o produto ao carrinho com quantidade inicial de 1
            itens[produto_id] = {
                "produto_id": produto["produto_id"],
                "nome": produto["nome"],
                "preco": produto["preco"],
                "quantidade": 1,
            }
    
    
    return HttpResponse(status=204)

    


def contatos(request):
     if not request.session.get('usuario_id'):
            return redirect('/')
     else:
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute('SELECT * FROM contatos where situacao!="Atendimento" AND situacao!="Finalizado";')
        contatos = cursor.fetchall()
        
        # Renderize o template HTML com os contatos recuperados
        return render(request, 'contatos.html', {"contatos": contatos})
def usuarios(request):
    if not request.session.get('usuario_id'):
            return redirect('/')
    else:
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute('SELECT * FROM usuarios;')
        usuarios = cursor.fetchall()
        
        # Renderize o template HTML com os contatos recuperados
        return render(request, 'usuarios.html', {"usuarios": usuarios})
def atenderchamado(request, id):
     if not request.session.get('usuario_id'):
            return redirect('/')
     else:
        usuario_id = request.session['usuario_id']

        try:
            # Connect to the database
            bd = conecta_no_banco_de_dados()
            cursor =  bd.cursor()

            # Update contato's status
            sql = 'UPDATE contatos SET situacao = %s WHERE id_contato = %s;'
            values = ("Atendimento", int(id))
            cursor.execute(sql, values)

            # Insert record into usuario_contato table
            sql = """
                INSERT INTO usuario_contato (usuario_id, contato_id, situacao)
                VALUES (%s, %s, %s);
            """
            values = (int(usuario_id), int(id), "Atendimento")
            cursor.execute(sql, values)

            # Commit changes and close connection
            bd.commit()
            bd.close()

            # Successful update
            return redirect('/paginainicial')

        except Exception as e:
            # Handle errors
            print(f"Erro ao atender chamado: {e}")
            return redirect('/contatos')  




def excluirususario(request,id):
    if not request.session.get('usuario_id'):
            return redirect('/')
    else:
        try:
            # Estabelecer conexão com o banco de dados (substitua 'seu_banco_de_dados' pelo nome real)
            bd =conecta_no_banco_de_dados()
            cursor = bd.cursor()

            # Evitar SQL injection usando parâmetros nomeados
            sql = 'DELETE FROM usuarios WHERE id = %(user_id)s;'
            params = {'user_id': id}

            cursor.execute(sql, params)
            bd.commit()
            cursor.close()

            messages.success(request, 'Usuário excluído com sucesso!')
            return redirect('paginainicial')

        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            messages.error(request, 'Falha ao excluir usuário. Tente novamente mais tarde.')
            return redirect('pagina_inicial')
def editarusuario(request,id):
    if not request.session.get('usuario_id'):
        return redirect('/')
    else:
        id_usuario = id
        bd = conecta_no_banco_de_dados()
        cursor = bd.cursor()
        cursor.execute("""
            SELECT id, nome, email
            FROM usuarios
            WHERE id = %s;
        """, (id,))
        dados_usuario = cursor.fetchone()
        cursor.close()
        bd.close()
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')    
            if not all([nome, email, senha]):
                return render(request, 'usuarios.html')
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            sql = (
                """
                UPDATE usuarios
                SET nome = %s, email = %s, senha = %s
                WHERE id = %s;
                """
            )
            values = (nome, email, senha, id)
            cursor.execute(sql, values)
            bd.commit()  # Assumindo que você tenha gerenciamento de transações
            cursor.close()
            bd.close()

            # Redirecione para a página de sucesso ou exiba a mensagem de confirmação
            return redirect('paginainicial')     

        # Exiba o formulário (assumindo lógica de renderização)
        return render(request, 'editarusuario.html',{'id': id_usuario})
def cadastro(request):
    if not request.session.get('usuario_id'):
        return redirect('/')
    else:
        if request.method == 'POST':
            nome = request.POST.get('nome')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            perfil = request.POST.get('perfil') 
          
      
            # Valide a entrada (assumindo lógica de validação)
            if not all([nome, email, senha,perfil]):
                # Lide com erros de validação (por exemplo, exiba mensagens de erro)
                return render(request, 'cadastro.html')

            # Atualize os dados do usuário se a validação for aprovada
            bd = conecta_no_banco_de_dados()
            cursor = bd.cursor()
            sql = (
                """
                INSERT INTO usuarios
                SET nome = %s, email = %s, senha = %s, perfil=%s;
                """
            )
            values = (nome, email, senha,perfil)
            cursor.execute(sql, values)
            bd.commit()  
            cursor.close()
            bd.close()

            # Redirecione para a página de sucesso ou exiba a mensagem de confirmação
            return redirect('paginainicial')     

        # Exiba o formulário (assumindo lógica de renderização)
        return render(request, 'cadastro.html')            






def index(request):
    if not request.session.get('usuario_id'):
        return redirect('/')
    else:
        return render(request, 'Guia/index.html')
def sobre(request):
    if not request.session.get('usuario_id'):
         return redirect('/')
    else:
        return render(request, 'Sobre/sobre.html')
def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            try:
                # Estabelecer conexão com o banco de dados
                bd = conecta_no_banco_de_dados()

                # Preparar consulta SQL e valores
                nome = form.cleaned_data['nome']
                email = form.cleaned_data['email']
                mensagem = form.cleaned_data['mensagem']
                sql = "INSERT INTO contatos (nome, email, mensagem) VALUES (%s, %s, %s)"
                values = (nome, email, mensagem)

                # Executar consulta SQL e confirmar alterações
                cursor = bd.cursor()
                cursor.execute(sql, values)
                bd.commit()

                # Mensagem de sucesso e redirecionamento
                print(f"Dados do formulário salvos com sucesso!")
                return HttpResponseRedirect('/')

            except Exception as err:
                # Manipular erros de banco de dados
                print(f"Erro ao salvar dados no banco de dados: {err}")
                mensagem_erro = "Ocorreu um erro ao processar o seu contato. Tente novamente mais tarde."
                return render(request, 'erro.html', mensagem_erro=mensagem_erro), 500

            finally:
                # Fechar conexão com o banco de dados se estiver aberta
                if bd is not None:
                    bd.close()

        else:
            # Manipular dados de formulário inválidos
            return render(request, 'contato.html', {'form': form})

    else:
        # Renderizar formulário vazio
        form = ContatoForm()
        return render(request, 'contato.html', {'form': form})
    