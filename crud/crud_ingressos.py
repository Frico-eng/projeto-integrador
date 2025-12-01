import mysql.connector
from mysql.connector import Error
from datetime import datetime

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

def inserir_ingresso(id_sessao, id_cliente, id_assento_sessao, valor):
    """
    Insere um novo ingresso na tabela Ingressos
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO Ingressos 
            (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_sessao, id_cliente, id_assento_sessao, valor, datetime.now()))
        
        con.commit()
        return cursor.lastrowid  # Retorna o ID do ingresso inserido
    except Error as e:
        print("Erro ao inserir ingresso:", e)
        return False
    finally:
        con.close()

def listar_ingressos():
    """
    Lista todos os ingressos do sistema
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                i.ID_Ingresso,
                i.ID_Sessao,
                f.Titulo_Filme,
                s.Data_Sessao,
                s.Hora_Sessao,
                sa.Nome_Sala,
                i.ID_Cliente,
                u.Nome as Nome_Cliente,
                i.ID_Assento_Sessao,
                a.Linha,
                a.Coluna,
                i.Valor,
                i.Data_Compra
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            LEFT JOIN Usuarios u ON i.ID_Cliente = u.ID_Usuario
            ORDER BY i.Data_Compra DESC
        """)
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar ingressos:", e)
        return []
    finally:
        con.close()

def listar_ingressos_por_cliente(id_cliente):
    """
    Lista todos os ingressos de um cliente específico
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                i.ID_Ingresso,
                i.ID_Sessao,
                f.Titulo_Filme,
                f.Duracao,
                f.Classificacao,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                sa.Nome_Sala,
                i.ID_Assento_Sessao,
                a.Linha,
                a.Coluna,
                i.Valor,
                i.Data_Compra
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE i.ID_Cliente = %s
            ORDER BY s.Data_Sessao DESC, s.Hora_Sessao DESC
        """, (id_cliente,))
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar ingressos do cliente:", e)
        return []
    finally:
        con.close()

def listar_ingressos_por_sessao(id_sessao):
    """
    Lista todos os ingressos de uma sessão específica
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                i.ID_Ingresso,
                i.ID_Cliente,
                u.Nome as Nome_Cliente,
                i.ID_Assento_Sessao,
                a.Linha,
                a.Coluna,
                i.Valor,
                i.Data_Compra
            FROM Ingressos i
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            LEFT JOIN Usuarios u ON i.ID_Cliente = u.ID_Usuario
            WHERE i.ID_Sessao = %s
            ORDER BY a.Linha, a.Coluna
        """, (id_sessao,))
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar ingressos da sessão:", e)
        return []
    finally:
        con.close()

def obter_ingresso_por_id(id_ingresso):
    """
    Obtém um ingresso específico pelo ID
    """
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                i.ID_Ingresso,
                i.ID_Sessao,
                f.Titulo_Filme,
                f.Duracao,
                f.Classificacao,
                f.Genero,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                sa.Nome_Sala,
                i.ID_Cliente,
                u.Nome as Nome_Cliente,
                u.Email,
                i.ID_Assento_Sessao,
                a.Linha,
                a.Coluna,
                i.Valor,
                i.Data_Compra
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            LEFT JOIN Usuarios u ON i.ID_Cliente = u.ID_Usuario
            WHERE i.ID_Ingresso = %s
        """, (id_ingresso,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao obter ingresso por ID:", e)
        return None
    finally:
        con.close()

def obter_resumo_vendas_sessao(id_sessao):
    """
    Retorna um resumo das vendas de uma sessão
    """
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_ingressos,
                SUM(Valor) as total_vendas,
                MIN(Data_Compra) as primeira_venda,
                MAX(Data_Compra) as ultima_venda
            FROM Ingressos 
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao obter resumo de vendas:", e)
        return None
    finally:
        con.close()

def inserir_multiplos_ingressos(lista_ingressos):
    """
    Insere múltiplos ingressos de uma vez (transação)
    Cada item da lista deve ser uma tupla: (id_sessao, id_cliente, id_assento_sessao, valor)
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        
        # Iniciar transação
        con.start_transaction()
        
        ids_ingressos = []
        for ingresso in lista_ingressos:
            id_sessao, id_cliente, id_assento_sessao, valor = ingresso
            
            cursor.execute("""
                INSERT INTO Ingressos 
                (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_sessao, id_cliente, id_assento_sessao, valor, datetime.now()))
            
            ids_ingressos.append(cursor.lastrowid)
        
        con.commit()
        return ids_ingressos  # Retorna lista com IDs dos ingressos inseridos
        
    except Error as e:
        print("Erro ao inserir múltiplos ingressos:", e)
        con.rollback()
        return False
    finally:
        con.close()

def verificar_ingresso_existente(id_sessao, id_assento_sessao):
    """
    Verifica se já existe um ingresso para uma sessão e assento específico
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT ID_Ingresso 
            FROM Ingressos 
            WHERE ID_Sessao = %s AND ID_Assento_Sessao = %s
        """, (id_sessao, id_assento_sessao))
        
        resultado = cursor.fetchone()
        return resultado is not None
    except Error as e:
        print("Erro ao verificar ingresso existente:", e)
        return False
    finally:
        con.close()