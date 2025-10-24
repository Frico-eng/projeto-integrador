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
    con = conectar()
    if con is None:
        return None
    
    cursor = con.cursor(dictionary=True)
    comando = "SELECT * FROM Usuarios WHERE Email = %s AND Senha = %s"
    cursor.execute(comando, (email, senha))
    usuario = cursor.fetchone()
    con.close()
    return usuario