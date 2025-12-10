# crud_filmes.py
import os
import mysql.connector
from mysql.connector import Error

# ========================= CONEXÃO MYSQL =========================
def conectar():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",         # Coloque seu usuário MySQL
            password="",         # Coloque sua senha MySQL
            database="cineplus"  # Certifique-se de criar este DB
        )
        return con
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None

# ========================= CRUD FILMES =========================
def inserir_filme(titulo, genero, duracao, classificacao, direcao, sinopse, cartaz_path=None):
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO Filmes (Titulo_Filme, Genero, Duracao, Classificacao, Direcao, Sinopse, Cartaz_Path) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, genero, duracao, classificacao, direcao, sinopse, cartaz_path))
        con.commit()
        return True
    except Error as e:
        print("Erro ao inserir filme:", e)
        return False
    finally:
        con.close()

def listar_filmes():
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT ID_Filme, Titulo_Filme, Genero, Duracao, Classificacao, Direcao, Sinopse, Cartaz_Path 
            FROM Filmes 
            ORDER BY ID_Filme ASC
        """)
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar filmes:", e)
        return []
    finally:
        con.close()

def editar_filme(id_filme, titulo, genero, duracao, classificacao, direcao, sinopse, cartaz_path=None):
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        if cartaz_path:
            cursor.execute("""
                UPDATE Filmes 
                SET Titulo_Filme=%s, Genero=%s, Duracao=%s, Classificacao=%s, Direcao=%s, Sinopse=%s, Cartaz_Path=%s 
                WHERE ID_Filme=%s
            """, (titulo, genero, duracao, classificacao, direcao, sinopse, cartaz_path, id_filme))
        else:
            cursor.execute("""
                UPDATE Filmes 
                SET Titulo_Filme=%s, Genero=%s, Duracao=%s, Classificacao=%s, Direcao=%s, Sinopse=%s 
                WHERE ID_Filme=%s
            """, (titulo, genero, duracao, classificacao, direcao, sinopse, id_filme))
        con.commit()
        return True
    except Error as e:
        print("Erro ao editar filme:", e)
        return False
    finally:
        con.close()

def excluir_filme(id_filme):
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Filmes WHERE ID_Filme=%s", (id_filme,))
        con.commit()
        return True
    except Error as e:
        print("Erro ao excluir filme:", e)
        return False
    finally:
        con.close()

def buscar_filme_por_id(id_filme):
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Filmes WHERE ID_Filme=%s", (id_filme,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao buscar filme:", e)
        return None
    finally:
        con.close()