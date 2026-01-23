# crud/crud_sala.py
from mysql.connector import Error
from conexao import conectar

def buscar_sala_por_id(id_sala):
    """Busca uma sala pelo ID"""
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Salas WHERE ID_Sala = %s", (id_sala,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao buscar sala:", e)
        return None
    finally:
        con.close()

def listar_salas():
    """Lista todas as salas"""
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Salas ORDER BY ID_Sala ASC")
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar salas:", e)
        return []
    finally:
        con.close()

def inserir_sala(nome_sala, capacidade):
    """Insere uma nova sala"""
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("INSERT INTO Salas (Nome_Sala, Capacidade) VALUES (%s, %s)", 
                      (nome_sala, capacidade))
        con.commit()
        return True
    except Error as e:
        print("Erro ao inserir sala:", e)
        return False
    finally:
        con.close()

def editar_sala(id_sala, nome_sala, capacidade):
    """Edita uma sala existente"""
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("UPDATE Salas SET Nome_Sala = %s, Capacidade = %s WHERE ID_Sala = %s", 
                      (nome_sala, capacidade, id_sala))
        con.commit()
        return True
    except Error as e:
        print("Erro ao editar sala:", e)
        return False
    finally:
        con.close()

def excluir_sala(id_sala):
    """Exclui uma sala"""
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Salas WHERE ID_Sala = %s", (id_sala,))
        con.commit()
        return True
    except Error as e:
        print("Erro ao excluir sala:", e)
        return False
    finally:
        con.close()

def buscar_sala_por_nome(nome_sala):
    """Busca uma sala pelo nome"""
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Salas WHERE Nome_Sala = %s", (nome_sala,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao buscar sala por nome:", e)
        return None
    finally:
        con.close()