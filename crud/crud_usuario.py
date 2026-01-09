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

def listar_usuarios():
    con = conectar()
    if con is None:
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Usuarios")
        usuarios = cursor.fetchall()
        return usuarios
    except Exception as e:
        print("Erro ao listar usuários:", e)
        return []
    finally:
        con.close()

def editar_usuario(id_usuario, nome, nome_login, senha, email=None, telefone=None, genero=None, data_nascimento=None, tipo_usuario='cliente'):
    con = conectar()
    if con is None:
        return False
    try:
        cursor = con.cursor()
        comando = """
            UPDATE Usuarios 
            SET Nome_Usuario = %s, Nome_Login = %s, Senha = %s, Email = %s, Telefone = %s, Genero = %s, Data_Nascimento = %s, Tipo_Usuario = %s
            WHERE ID_Usuario = %s
        """
        valores = (nome, nome_login, senha, email, telefone, genero, data_nascimento, tipo_usuario, id_usuario)
        cursor.execute(comando, valores)
        con.commit()
        return True
    except Exception as e:
        print("Erro ao editar usuário:", e)
        return False
    finally:
        con.close()

def excluir_usuario(id_usuario):
    con = conectar()
    if con is None:
        return False
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE ID_Usuario = %s", (id_usuario,))
        con.commit()
        return True
    except Exception as e:
        print("Erro ao excluir usuário:", e)
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