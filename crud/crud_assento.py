from conexao import conectar

def buscar_assentos_sessao(id_sessao):
    """
    Busca todos os assentos de uma sessão específica com status de disponibilidade
    """
    try:
        conn = conectar()
        if conn is None:
            print("Erro: Não foi possível conectar ao banco de dados")
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        # Query para buscar assentos com status de disponibilidade
        cursor.execute('''
            SELECT 
                a.ID_Assento,
                a.Linha,
                a.Coluna,
                CASE 
                    WHEN i.ID_Ingresso IS NULL THEN 'disponivel'
                    ELSE 'ocupado'
                END AS Status
            FROM Sessoes s
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            INNER JOIN Assentos a ON sa.ID_Sala = a.ID_Sala
            LEFT JOIN Ingressos i ON a.ID_Assento = i.ID_Assento AND i.ID_Sessao = s.ID_Sessao
            WHERE s.ID_Sessao = %s
            ORDER BY a.Linha, a.Coluna
        ''', (id_sessao,))
        
        assentos = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return assentos
        
    except Exception as e:
        print(f"Erro ao buscar assentos: {e}")
        return None

def buscar_informacoes_sessao(id_sessao):
    """
    Busca informações completas da sessão (filme, sala, horário, etc.)
    """
    try:
        conn = conectar()
        if conn is None:
            print("Erro: Não foi possível conectar ao banco de dados")
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            SELECT 
                s.ID_Sessao,
                f.Titulo AS Filme,
                f.Duracao,
                f.Classificacao,
                f.Imagem,
                sa.Nome AS Sala,
                sa.Capacidade,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao
            FROM Sessoes s
            INNER JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Sessao = %s
        ''', (id_sessao,))
        
        sessao = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return sessao
        
    except Exception as e:
        print(f"Erro ao buscar informações da sessão: {e}")
        return None

def buscar_sessoes_filme(id_filme, data=None):
    """
    Busca todas as sessões disponíveis para um filme
    """
    try:
        conn = conectar()
        if conn is None:
            print("Erro: Não foi possível conectar ao banco de dados")
            return None
            
        cursor = conn.cursor(dictionary=True)
        
        if data:
            cursor.execute('''
                SELECT 
                    s.ID_Sessao,
                    s.Data_Sessao,
                    s.Hora_Sessao,
                    s.Tipo_Sessao,
                    sa.Nome AS Sala,
                    sa.Capacidade
                FROM Sessoes s
                INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
                WHERE s.ID_Filme = %s AND s.Data_Sessao = %s
                ORDER BY s.Data_Sessao, s.Hora_Sessao
            ''', (id_filme, data))
        else:
            cursor.execute('''
                SELECT 
                    s.ID_Sessao,
                    s.Data_Sessao,
                    s.Hora_Sessao,
                    s.Tipo_Sessao,
                    sa.Nome AS Sala,
                    sa.Capacidade
                FROM Sessoes s
                INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
                WHERE s.ID_Filme = %s
                ORDER BY s.Data_Sessao, s.Hora_Sessao
            ''', (id_filme,))
        
        sessoes = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return sessoes
        
    except Exception as e:
        print(f"Erro ao buscar sessões: {e}")
        return None