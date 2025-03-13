import mysql.connector

def conecta_no_banco_de_dados():
    
    cnx = mysql.connector.connect(host='localhost', user='root', password='')

   
    cursor = cnx.cursor()

    
    cursor.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "nozama";')
    num_results = cursor.fetchone()[0]

    
    cnx.close()

    
    if num_results == 0:
        
        cnx = mysql.connector.connect(host='localhost', user='root', password='')

        cursor = cnx.cursor()
        cursor.execute('CREATE DATABASE nozama;')
        cnx.commit()

        
        cnx = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nozama'  
        )

        cursor = cnx.cursor()

        
        cursor.execute('''
            CREATE TABLE produtos (
                produto_id INT AUTO_INCREMENT PRIMARY KEY, 
                nome VARCHAR(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
                preco DECIMAL(10, 2) NOT NULL,
                imagem VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL);''')    
            
        

        
        cursor.execute('''
            CREATE TABLE usuarios (
                usuario_id INT AUTO_INCREMENT PRIMARY KEY, 
                nome VARCHAR(255), 
                email VARCHAR(255) UNIQUE, 
                senha VARCHAR(255), 
                perfil VARCHAR(255)
            );
        ''')

        
        cursor.execute(''' 
            CREATE TABLE usuario_compras (
                usuario_id INT NOT NULL, 
                produto_id INT NOT NULL,
                data_compra TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
                PRIMARY KEY (usuario_id, produto_id), 
                FOREIGN KEY (usuario_id) REFERENCES usuarios(usuario_id) ON DELETE CASCADE, 
                FOREIGN KEY (produto_id) REFERENCES produtos(produto_id) ON DELETE CASCADE
            );
        ''')

        cursor.execute('''
            INSERT INTO produtos (produto_id, nome, preco, imagem)
            VALUES 
            (1, 'Elefante Psíquico de Guerra Pré-Histórico', 100.00, 'produto 1.jpeg'),
            (2, 'Lâmina do Caos', 150.00, 'produto 2.jpeg'),
            (3, 'Livro Misterioso', 200.00, 'produto 3.jpg')
        ''')

       
        nome = "Professor Lucas"
        email = "peres@peres.com"
        senha = "12345"
        perfil = "administrador"
        sql = "INSERT INTO usuarios (nome, email, senha, perfil) VALUES (%s, %s, %s, %s)"
        valores = (nome, email, senha, perfil)
        cursor.execute(sql, valores)
        cnx.commit()
     
        
        cnx.close()
        
    try:
        
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