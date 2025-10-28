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