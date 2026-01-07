import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="cineplus"
        )
        return con
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

def listar_assentos_por_sala(id_sala):
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT ID_Assento, ID_Sala, Linha, Coluna, Status 
            FROM Assentos 
            WHERE ID_Sala = %s 
            ORDER BY Linha, Coluna
        """, (id_sala,))
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar assentos:", e)
        return []
    finally:
        con.close()

def atualizar_status_assento(id_assento, status):
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("UPDATE Assentos SET Status = %s WHERE ID_Assento = %s", 
                      (status, id_assento))
        con.commit()
        return True
    except Error as e:
        print("Erro ao atualizar assento:", e)
        return False
    finally:
        con.close()

def buscar_assento_sessao_por_numero(id_sessao, fileira, numero):
    conexao = conectar()
    if conexao is None:
        return None
    
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT ass.ID_Assento_Sessao
            FROM Assentos_Sessao ass
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE ass.ID_Sessao = %s 
            AND a.Fileira_Assento = %s 
            AND a.Numero_Assento = %s
        """, (id_sessao, fileira, numero))
        
        resultado = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        return resultado[0] if resultado else None
        
    except Error as e:
        print("Erro ao buscar assento_sessao:", e)
        if conexao:
            conexao.close()
        return None