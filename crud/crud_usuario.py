from conexao import conectar

def inserir_usuario(nome, nome_login, senha, email=None, telefone=None, genero=None, data_nascimento=None, tipo_usuario='cliente'):
    con = conectar()
    if con is None:
        return False
    try:
        cursor = con.cursor()
        comando = """
            INSERT INTO Usuarios 
            (Nome_Usuario, Nome_Login, Senha, Email, Telefone, Genero, Data_Nascimento, Tipo_Usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (nome, nome_login, senha, email, telefone, genero, data_nascimento, tipo_usuario)
        print("Comando SQL:", comando)
        print("Valores:", valores)
        cursor.execute(comando, valores)
        con.commit()
        return True
    except Exception as e:
        print("Erro ao inserir usuário:", e)
        return False
    finally:
        con.close()

def verificar_login(email, senha):
    """
    Verifica as credenciais de login e retorna os dados do usuário incluindo o tipo
    """
    try:
        conn = conectar()
        if conn is None:
            print("Erro: Não foi possível conectar ao banco de dados")
            return None
            
        cursor = conn.cursor(dictionary=True)  # Para retornar dicionários
        
        cursor.execute('''
            SELECT ID_Usuario, Nome_Usuario, Email, Tipo_Usuario 
            FROM Usuarios 
            WHERE Email = %s AND Senha = %s
        ''', (email, senha))
        
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if usuario:
            return {
                "ID_Usuario": usuario["ID_Usuario"],
                "Nome_Usuario": usuario["Nome_Usuario"],
                "Email": usuario["Email"],
                "Tipo_Usuario": usuario["Tipo_Usuario"]  # "cliente" ou "funcionario"
            }
        return None
        
    except Exception as e:
        print(f"Erro ao verificar login: {e}")
        return None