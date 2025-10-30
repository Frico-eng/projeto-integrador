# crud/crud_sessao.py
import mysql.connector
from mysql.connector import Error
from datetime import datetime, time

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



def listar_sessoes_por_filme(id_filme):
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ID_Sessao, 
                ID_Filme, 
                ID_Sala, 
                Data_Sessao, 
                Hora_Sessao,
                Tipo_Sessao 
            FROM Sessoes 
            WHERE ID_Filme = %s
            ORDER BY Hora_Sessao ASC
        """, (id_filme,))
        resultado = cursor.fetchall()
        
        # Converter timedelta para string de hora formatada
        for sessao in resultado:
            hora = sessao['Hora_Sessao']
            
            if hasattr(hora, 'total_seconds'):
                # É um timedelta - converter para HH:MM
                total_seconds = int(hora.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                sessao['Hora_Formatada'] = f"{hours:02d}:{minutes:02d}"
            elif hasattr(hora, 'strftime'):
                # É um datetime.time - formatar normalmente
                sessao['Hora_Formatada'] = hora.strftime("%H:%M")
            else:
                # Fallback
                sessao['Hora_Formatada'] = str(hora)
        
        return resultado
    except Error as e:
        print("Erro ao listar sessões:", e)
        return []
    finally:
        con.close()

def buscar_sessao_por_dados(id_filme, data_sessao, horario_sessao, tipo_sessao):
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ID_Sessao, 
                ID_Filme, 
                ID_Sala, 
                Data_Sessao, 
                TIME_FORMAT(Hora_Sessao, '%%H:%%i') as Hora_Formatada,
                Tipo_Sessao 
            FROM Sessoes 
            WHERE ID_Filme = %s 
            AND Data_Sessao = %s 
            AND TIME_FORMAT(Hora_Sessao, '%%H:%%i') = %s 
            AND Tipo_Sessao = %s
        """, (id_filme, data_sessao, horario_sessao, tipo_sessao))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao buscar sessão:", e)
        return None
    finally:
        con.close()