from mysql.connector import Error
from datetime import datetime
from conexao import conectar

def listar_assentos_por_sessao(id_sessao):

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

def obter_assentos_com_ingressos(id_sessao):
    """
    Retorna lista de IDs de assentos que possuem ingressos comprados para uma sessão.
    Esta é a fonte de verdade para assentos ocupados no sistema.
    
    Args:
        id_sessao: ID da sessão
    
    Returns:
        Lista de IDs de Assentos (ID_Assento) que têm ingressos
    """
    con = conectar()
    if con is None:
        return []
    
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT DISTINCT ass.ID_Assento
            FROM Ingressos i
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            WHERE i.ID_Sessao = %s
        """, (id_sessao,))
        
        resultados = cursor.fetchall()
        ids_assentos = [resultado[0] for resultado in resultados]
        
        cursor.close()
        con.close()
        
        return ids_assentos
        
    except Error as e:
        print(f"Erro ao obter assentos com ingressos: {e}")
        return []

def sincronizar_assentos_com_ingressos(id_sessao):
    """
    Sincroniza o status dos assentos na tabela Assentos_Sessao com base nos ingressos comprados.
    Marca como 'ocupado' todos os assentos que têm ingressos, e libera os que não têm.
    
    Args:
        id_sessao: ID da sessão a sincronizar
    
    Returns:
        True se sincronização foi bem-sucedida, False caso contrário
    """
    con = conectar()
    if con is None:
        return False
    
    try:
        cursor = con.cursor()
        
        # Iniciar transação para garantir consistência
        con.start_transaction()
        
        # Obter lista de assentos que têm ingressos
        cursor.execute("""
            SELECT DISTINCT ass.ID_Assento_Sessao, ass.ID_Assento
            FROM Ingressos i
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            WHERE i.ID_Sessao = %s
        """, (id_sessao,))
        
        assentos_com_ingresso = cursor.fetchall()
        ids_assentos_ocupados = [assento[1] for assento in assentos_com_ingresso]
        
        # Marcar todos os assentos como 'disponivel' primeiro
        cursor.execute("""
            UPDATE Assentos_Sessao 
            SET Status = 'disponivel', 
                ID_Cliente = NULL,
                Data_Hora_Reserva = NULL
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        
        # Marcar como 'ocupado' os assentos que têm ingressos
        for id_assento in ids_assentos_ocupados:
            # Obter informações do cliente e data do ingresso
            cursor.execute("""
                SELECT i.ID_Cliente, MAX(i.Data_Compra) as data_compra
                FROM Ingressos i
                JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
                WHERE i.ID_Sessao = %s AND ass.ID_Assento = %s
                GROUP BY i.ID_Cliente
            """, (id_sessao, id_assento))
            
            info_ingresso = cursor.fetchone()
            
            if info_ingresso:
                id_cliente, data_compra = info_ingresso
                
                cursor.execute("""
                    UPDATE Assentos_Sessao 
                    SET Status = 'ocupado', 
                        ID_Cliente = %s,
                        Data_Hora_Reserva = %s
                    WHERE ID_Sessao = %s AND ID_Assento = %s
                """, (id_cliente, data_compra, id_sessao, id_assento))
        
        con.commit()
        print(f"✓ Sincronização concluída para sessão {id_sessao}: {len(ids_assentos_ocupados)} assentos marcados como ocupados")
        return True
        
    except Error as e:
        print(f"Erro ao sincronizar assentos com ingressos: {e}")
        con.rollback()
        return False
    finally:
        con.close()

def verificar_assento_ocupado_por_ingresso(id_sessao, id_assento):
    """
    Verifica se um assento específico tem ingresso comprado (está realmente ocupado).
    Esta é a verificação mais confiável baseada em ingressos efetivos.
    
    Args:
        id_sessao: ID da sessão
        id_assento: ID do assento base
    
    Returns:
        True se existe ingresso para este assento, False caso contrário
    """
    con = conectar()
    if con is None:
        return False
    
    try:
        cursor = con.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM Ingressos i
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            WHERE i.ID_Sessao = %s AND ass.ID_Assento = %s
        """, (id_sessao, id_assento))
        
        resultado = cursor.fetchone()
        total = resultado[0] if resultado else 0
        
        cursor.close()
        con.close()
        
        return total > 0
        
    except Error as e:
        print(f"Erro ao verificar assento ocupado por ingresso: {e}")
        return False

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