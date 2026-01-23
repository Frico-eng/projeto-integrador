# crud/crud_sessao_assento.py
"""
Arquivo integrado para operações envolvendo Sessões e Assentos
Facilita a verificação de disponibilidade em tempo real
"""
from mysql.connector import Error
from datetime import datetime
from conexao import conectar

def obter_sessao_completa(id_sessao):
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        
        # Buscar informações da sessão
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                s.ID_Filme,
                s.ID_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                f.Titulo_Filme,
                f.Duracao,
                f.Classificacao,
                f.Cartaz_Path,
                sa.Nome_Sala,
                sa.Capacidade
            FROM Sessoes s
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Sessao = %s
        """, (id_sessao,))
        
        sessao_info = cursor.fetchone()
        
        if not sessao_info:
            return None
        
        # Buscar resumo de ocupação
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN Status = 'disponivel' THEN 1 ELSE 0 END) as disponiveis,
                SUM(CASE WHEN Status = 'ocupado' THEN 1 ELSE 0 END) as ocupados,
                COUNT(*) as total
            FROM Assentos_Sessao 
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        
        ocupacao = cursor.fetchone()
        
        if ocupacao:
            sessao_info['assentos_disponiveis'] = ocupacao['disponiveis'] or 0
            sessao_info['assentos_ocupados'] = ocupacao['ocupados'] or 0
            sessao_info['total_assentos'] = ocupacao['total'] or 0
            
            # Calcular taxa de ocupação
            if ocupacao['total']:
                sessao_info['taxa_ocupacao'] = (ocupacao['ocupados'] or 0) / ocupacao['total'] * 100
                sessao_info['taxa_disponibilidade'] = (ocupacao['disponiveis'] or 0) / ocupacao['total'] * 100
            else:
                sessao_info['taxa_ocupacao'] = 0
                sessao_info['taxa_disponibilidade'] = 0
        
        return sessao_info
    except Error as e:
        print("Erro ao obter sessão completa:", e)
        return None
    finally:
        con.close()

def verificar_disponibilidade_sessao(id_filme, tipo_sessao, hora_sessao, id_sala=None):
    """
    Verifica se uma sessão específica tem assentos disponíveis
    
    Returns:
        dict com: disponivel (bool), assentos_livres (int), total_assentos (int), 
                  id_sessao, taxa_ocupacao (%)
    """
    con = conectar()
    if con is None: 
        return {"disponivel": False, "motivo": "Erro de conexão"}
    
    try:
        cursor = con.cursor(dictionary=True)
        
        # Buscar a sessão
        query = """
            SELECT s.ID_Sessao
            FROM Sessoes s
            WHERE s.ID_Filme = %s 
            AND s.Tipo_Sessao = %s 
            AND TIME(s.Hora_Sessao) = %s
        """
        params = [id_filme, tipo_sessao, hora_sessao]
        
        if id_sala:
            query += " AND s.ID_Sala = %s"
            params.append(id_sala)
        
        cursor.execute(query, params)
        sessao = cursor.fetchone()
        
        if not sessao:
            return {
                "disponivel": False,
                "motivo": "Sessão não encontrada",
                "assentos_livres": 0,
                "total_assentos": 0,
                "taxa_ocupacao": 100
            }
        
        id_sessao = sessao['ID_Sessao']
        
        # Verificar ocupação
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN Status = 'disponivel' THEN 1 ELSE 0 END) as disponiveis,
                COUNT(*) as total
            FROM Assentos_Sessao 
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        
        ocupacao = cursor.fetchone()
        
        disponiveis = ocupacao['disponiveis'] or 0
        total = ocupacao['total'] or 0
        
        return {
            "disponivel": disponiveis > 0,
            "id_sessao": id_sessao,
            "assentos_livres": disponiveis,
            "total_assentos": total,
            "taxa_ocupacao": ((total - disponiveis) / total * 100) if total > 0 else 0,
            "motivo": "Sessão cheia" if disponiveis == 0 else "OK"
        }
    except Error as e:
        print("Erro ao verificar disponibilidade da sessão:", e)
        return {"disponivel": False, "motivo": f"Erro: {str(e)}"}
    finally:
        con.close()

def obter_sessoes_com_disponibilidade(id_filme, tipo_sessao):
    """
    Obtém todas as sessões de um filme com informações de disponibilidade
    
    Returns:
        Lista de dicts com: ID_Sessao, Hora_Sessao, Tipo_Sessao, assentos_livres, 
                           total_assentos, taxa_ocupacao, disponivel
    """
    con = conectar()
    if con is None: 
        return []
    
    try:
        cursor = con.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT DISTINCT
                s.ID_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                sa.Nome_Sala,
                s.ID_Sala
            FROM Sessoes s
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Filme = %s 
            AND s.Tipo_Sessao = %s
            ORDER BY s.Hora_Sessao ASC
        """, (id_filme, tipo_sessao))
        
        sessoes = cursor.fetchall()
        
        # Adicionar informações de disponibilidade para cada sessão
        for sessao in sessoes:
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN Status = 'disponivel' THEN 1 ELSE 0 END) as disponiveis,
                    COUNT(*) as total
                FROM Assentos_Sessao 
                WHERE ID_Sessao = %s
            """, (sessao['ID_Sessao'],))
            
            ocupacao = cursor.fetchone()
            disponiveis = ocupacao['disponiveis'] or 0
            total = ocupacao['total'] or 0
            
            sessao['assentos_livres'] = disponiveis
            sessao['total_assentos'] = total
            sessao['disponivel'] = disponiveis > 0
            sessao['taxa_ocupacao'] = ((total - disponiveis) / total * 100) if total > 0 else 0
        
        return sessoes
    except Error as e:
        print("Erro ao obter sessões com disponibilidade:", e)
        return []
    finally:
        con.close()

def alertar_pouca_disponibilidade(id_sessao, limite=10):
    """
    Verifica se uma sessão está com poucos assentos disponíveis
    
    Returns:
        tuple (alerta_ativo: bool, assentos_livres: int)
    """
    con = conectar()
    if con is None: 
        return False, 0
    
    try:
        cursor = con.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                SUM(CASE WHEN Status = 'disponivel' THEN 1 ELSE 0 END) as disponiveis
            FROM Assentos_Sessao 
            WHERE ID_Sessao = %s
        """, (id_sessao,))
        
        resultado = cursor.fetchone()
        disponiveis = resultado['disponiveis'] or 0
        
        return disponiveis <= limite, disponiveis
    except Error as e:
        print("Erro ao alertar pouca disponibilidade:", e)
        return False, 0
    finally:
        con.close()
