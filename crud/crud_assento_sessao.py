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

def listar_assentos_por_sessao(id_sessao):
    """
    Lista todos os assentos de uma sessão específica com seus status
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ass.ID_Assento_Sessao,
                a.ID_Assento,
                a.Linha,
                a.Coluna,
                ass.Status,
                ass.ID_Cliente,
                ass.Data_Hora_Reserva
            FROM Assentos_Sessao ass
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE ass.ID_Sessao = %s 
            ORDER BY a.Linha, a.Coluna
        """, (id_sessao,))
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar assentos da sessão:", e)
        return []
    finally:
        con.close()

def listar_assentos_disponiveis_por_sessao(id_sessao):
    """
    Lista apenas os assentos disponíveis de uma sessão
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                ass.ID_Assento_Sessao,
                a.ID_Assento,
                a.Linha,
                a.Coluna
            FROM Assentos_Sessao ass
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE ass.ID_Sessao = %s AND ass.Status = 'disponivel'
            ORDER BY a.Linha, a.Coluna
        """, (id_sessao,))
        resultado = cursor.fetchall()
        return resultado
    except Error as e:
        print("Erro ao listar assentos disponíveis:", e)
        return []
    finally:
        con.close()

def reservar_assento(id_sessao, id_assento, id_cliente=None):
    """
    Reserva um assento específico para uma sessão
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE Assentos_Sessao 
            SET Status = 'ocupado', 
                ID_Cliente = %s,
                Data_Hora_Reserva = %s
            WHERE ID_Sessao = %s 
            AND ID_Assento = %s 
            AND Status = 'disponivel'
        """, (id_cliente, datetime.now(), id_sessao, id_assento))
        
        linhas_afetadas = cursor.rowcount
        con.commit()
        
        return linhas_afetadas > 0
    except Error as e:
        print("Erro ao reservar assento:", e)
        return False
    finally:
        con.close()

def liberar_assento(id_sessao, id_assento):
    """
    Libera um assento reservado (marca como disponível)
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE Assentos_Sessao 
            SET Status = 'disponivel', 
                ID_Cliente = NULL,
                Data_Hora_Reserva = NULL
            WHERE ID_Sessao = %s AND ID_Assento = %s
        """, (id_sessao, id_assento))
        
        linhas_afetadas = cursor.rowcount
        con.commit()
        
        return linhas_afetadas > 0
    except Error as e:
        print("Erro ao liberar assento:", e)
        return False
    finally:
        con.close()

def verificar_disponibilidade_assento(id_sessao, id_assento):
    """
    Verifica se um assento específico está disponível em uma sessão
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT Status 
            FROM Assentos_Sessao 
            WHERE ID_Sessao = %s AND ID_Assento = %s
        """, (id_sessao, id_assento))
        
        resultado = cursor.fetchone()
        return resultado and resultado['Status'] == 'disponivel'
    except Error as e:
        print("Erro ao verificar disponibilidade:", e)
        return False
    finally:
        con.close()

def obter_info_sessao(id_sessao):
    """
    Obtém informações completas sobre uma sessão
    """
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                f.Titulo_Filme,
                f.Duracao,
                f.Classificacao,
                sa.Nome_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao
            FROM Sessoes s
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Sessao = %s
        """, (id_sessao,))
        
        return cursor.fetchone()
    except Error as e:
        print("Erro ao obter informações da sessão:", e)
        return None
    finally:
        con.close()

def obter_resumo_ocupacao_sessao(id_sessao):
    """
    Retorna um resumo da ocupação da sessão
    """
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) as total_assentos,
                SUM(CASE WHEN Status = 'disponivel' THEN 1 ELSE 0 END) as disponiveis,
                SUM(CASE WHEN Status = 'ocupado' THEN 1 ELSE 0 END) as ocupados,
                SUM(CASE WHEN Status = 'reservado' THEN 1 ELSE 0 END) as reservados
            FROM Assentos_Sessao 
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        
        return cursor.fetchone()
    except Error as e:
        print("Erro ao obter resumo de ocupação:", e)
        return None
    finally:
        con.close()

def reservar_multiplos_assentos(id_sessao, lista_assentos, id_cliente=None):
    """
    Reserva múltiplos assentos de uma vez (transação)
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        
        # Iniciar transação
        con.start_transaction()
        
        # Verificar se todos os assentos estão disponíveis
        for id_assento in lista_assentos:
            cursor.execute("""
                SELECT Status 
                FROM Assentos_Sessao 
                WHERE ID_Sessao = %s AND ID_Assento = %s
            """, (id_sessao, id_assento))
            
            resultado = cursor.fetchone()
            if not resultado or resultado[0] != 'disponivel':
                con.rollback()
                return False
        
        # Reservar todos os assentos
        for id_assento in lista_assentos:
            cursor.execute("""
                UPDATE Assentos_Sessao 
                SET Status = 'ocupado', 
                    ID_Cliente = %s,
                    Data_Hora_Reserva = %s
                WHERE ID_Sessao = %s AND ID_Assento = %s
            """, (id_cliente, datetime.now(), id_sessao, id_assento))
        
        con.commit()
        return True
        
    except Error as e:
        print("Erro ao reservar múltiplos assentos:", e)
        con.rollback()
        return False
    finally:
        con.close()

# Exemplos de uso:
if __name__ == "__main__":
    # Exemplo 1: Listar assentos de uma sessão
    print("=== Assentos da Sessão 1 ===")
    assentos = listar_assentos_por_sessao(1)
    for assento in assentos:
        print(f"Assento {assento['Linha']}{assento['Coluna']}: {assento['Status']}")
    
    # Exemplo 2: Obter informações da sessão
    print("\n=== Informações da Sessão ===")
    sessao_info = obter_info_sessao(1)
    if sessao_info:
        print(f"Filme: {sessao_info['Titulo_Filme']}")
        print(f"Sala: {sessao_info['Nome_Sala']}")
        print(f"Data: {sessao_info['Data_Sessao']} {sessao_info['Hora_Sessao']}")
    
    # Exemplo 3: Reservar um assento
    print("\n=== Reservando assento ===")
    if reservar_assento(1, 1, 1):  # Sessão 1, Assento 1, Cliente 1
        print("Assento reservado com sucesso!")
    else:
        print("Falha ao reservar assento")
    
    # Exemplo 4: Verificar resumo de ocupação
    print("\n=== Resumo de Ocupação ===")
    resumo = obter_resumo_ocupacao_sessao(1)
    if resumo:
        print(f"Total: {resumo['total_assentos']}")
        print(f"Disponíveis: {resumo['disponiveis']}")
        print(f"Ocupados: {resumo['ocupados']}")