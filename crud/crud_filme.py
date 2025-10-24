# cineplus_crud.py
import os
import customtkinter as ctk
from tkinter import ttk
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


def inserir_filme(titulo, ano, genero, duracao):
    con = conectar()
    if con is None: return False
    cursor = con.cursor()
    cursor.execute("INSERT INTO filmes (titulo, ano, genero, duracao) VALUES (%s,%s,%s,%s)",
                   (titulo, ano, genero, duracao))
    con.commit()
    con.close()
    return True

def listar_filmes():
    con = conectar()
    if con is None: return []
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM filmes ORDER BY titulo ASC")
    resultado = cursor.fetchall()
    con.close()
    return resultado

def editar_filme(id_filme, titulo, ano, genero, duracao):
    con = conectar()
    if con is None: return False
    cursor = con.cursor()
    cursor.execute("UPDATE filmes SET titulo=%s, ano=%s, genero=%s, duracao=%s WHERE id=%s",
                   (titulo, ano, genero, duracao, id_filme))
    con.commit()
    con.close()
    return True

def excluir_filme(id_filme):
    con = conectar()
    if con is None: return False
    cursor = con.cursor()
    cursor.execute("DELETE FROM filmes WHERE id=%s", (id_filme,))
    con.commit()
    con.close()
    return True

