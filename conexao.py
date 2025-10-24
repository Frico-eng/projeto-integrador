# conexao.py
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",           # seu usuário MySQL
            password="",     # altere para sua senha
            database="cineplus"
        )
        return conexao
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return None