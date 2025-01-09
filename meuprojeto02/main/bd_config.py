import mysql.connector

def conecta_no_banco_de_dados():
    # Conectar ao servidor MySQL
    cnx = mysql.connector.connect(host='localhost', user='root', password='')

    # Criar o cursor para interagir com o banco de dados
    cursor = cnx.cursor()

    # Verificar se o banco de dados 'nozama' existe
    cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "nozama";')
    num_results = cursor.fetchone()[0]

    # Fechar a conexão inicial
    cnx.close()

    # Se o banco de dados não existe, criá-lo
    if num_results == 0:
        # Conectar-se novamente ao servidor MySQL para criar o banco de dados
        cnx = mysql.connector.connect(host='localhost', user='root', password='')

        cursor = cnx.cursor()
        cursor.execute('CREATE DATABASE nozama;')
        cnx.commit()

        # Conectar-se ao banco de dados recém-criado
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nozama'  # Especificar o banco de dados
        )

        cursor = cnx.cursor()

        # criar tabela de produtos
        cursor.execute('''
            CREATE TABLE produtos (
                produto_id INT AUTO_INCREMENT PRIMARY KEY, 
                nome VARCHAR(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                imagem VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL);''')    
            
        

        # Criar a tabela de usuarios com a coluna 'perfil'
        cursor.execute('''
            CREATE TABLE usuarios (
                usuario_id INT AUTO_INCREMENT PRIMARY KEY, 
                nome VARCHAR(255), 
                email VARCHAR(255) UNIQUE, 
                senha VARCHAR(255), 
                perfil VARCHAR(255)
            );
        ''')

        # Criar a tabela de relacionamento entre usuários e produtos
        cursor.execute(''' 
            CREATE TABLE usuario_compras (
                usuario_id INT NOT NULL, 
                produto_id INT NOT NULL,  
                PRIMARY KEY (usuario_id, produto_id), 
                FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE, 
                FOREIGN KEY (produto_id) REFERENCES produtos(produto_id) ON DELETE CASCADE
            );
        ''')

        # Inserir dados iniciais na tabela 'usuarios'
        nome = "Professor Lucas"
        email = "peres@peres.com"
        senha = "12345"
        perfil = "administrador"
        sql = "INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, senha, perfil)
        cursor.execute(sql, valores)
        cnx.commit()
     
        # Fechar a conexão
        cnx.close()
        
    try:
        # Conectar ao banco de dados 'nozama' existente
        bd = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nozama'
        )
    except mysql.connector.Error as err:
        print("Erro de conexão com o banco de dados:", err)
        raise

    return bd