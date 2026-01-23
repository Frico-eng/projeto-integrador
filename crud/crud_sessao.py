# crud/crud_sessao.py
from mysql.connector import Error
from datetime import datetime, time, timedelta
from conexao import conectar

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

def listar_sessoes_por_dia_horario(dia_info, horario):
    """
    Lista todas as sessões disponíveis para um dia e horário específicos
    
    Args:
        dia_info: dict com informações do dia {'data': datetime, 'label': 'dd/mm', 'nome': 'Dia'}
        horario: string no formato 'HH:MM'
    
    Returns:
        Lista de sessões com informações completas
    """
    con = conectar()
    if con is None: 
        return []
    
    try:
        cursor = con.cursor(dictionary=True)
        
        # Converter a data do formato brasileiro para o formato do banco (YYYY-MM-DD)
        data_sessao = dia_info['data'].strftime('%Y-%m-%d')
        
        # Buscar sessões para a data e horário específicos
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                s.ID_Filme,
                s.ID_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                f.Titulo_Filme,
                f.Genero,
                f.Duracao,
                f.Classificacao,
                f.Cartaz_Path,
                f.Direcao,
                f.Sinopse,
                sa.Nome_Sala,
                sa.Capacidade
            FROM Sessoes s
            INNER JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.Data_Sessao = %s 
            AND TIME_FORMAT(s.Hora_Sessao, '%%H:%%i') = %s
            ORDER BY f.Titulo_Filme ASC
        """, (data_sessao, horario))
        
        resultado = cursor.fetchall()
        
        # Formatar os dados das sessões
        sessoes_formatadas = []
        for sessao in resultado:
            # Formatar hora
            hora = sessao['Hora_Sessao']
            if hasattr(hora, 'total_seconds'):
                total_seconds = int(hora.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                hora_formatada = f"{hours:02d}:{minutes:02d}"
            elif hasattr(hora, 'strftime'):
                hora_formatada = hora.strftime("%H:%M")
            else:
                hora_formatada = str(hora)
            
            sessao_formatada = {
                "ID_Sessao": sessao["ID_Sessao"],
                "ID_Filme": sessao["ID_Filme"],
                "ID_Sala": sessao["ID_Sala"],
                "Data_Sessao": sessao["Data_Sessao"],
                "Hora_Sessao": sessao["Hora_Sessao"],
                "Hora_Formatada": hora_formatada,
                "Tipo_Sessao": sessao["Tipo_Sessao"],
                "Titulo_Filme": sessao["Titulo_Filme"],
                "Genero": sessao["Genero"],
                "Duracao": sessao["Duracao"],
                "Classificacao": sessao["Classificacao"],
                "Cartaz_Path": sessao["Cartaz_Path"],
                "Direcao": sessao["Direcao"],
                "Sinopse": sessao["Sinopse"],
                "Nome_Sala": sessao["Nome_Sala"],
                "Capacidade": sessao["Capacidade"]
            }
            sessoes_formatadas.append(sessao_formatada)
        
        return sessoes_formatadas
        
    except Error as e:
        print("Erro ao listar sessões por dia/horário:", e)
        return []
    finally:
        con.close()

def listar_horarios_disponiveis_por_dia(dia_info):
    """
    Lista todos os horários disponíveis para um dia específico
    
    Args:
        dia_info: dict com informações do dia {'data': datetime, 'label': 'dd/mm', 'nome': 'Dia'}
    
    Returns:
        Lista de horários únicos no formato 'HH:MM'
    """
    con = conectar()
    if con is None: 
        return []
    
    try:
        cursor = con.cursor()
        
        # Converter a data para o formato do banco
        data_sessao = dia_info['data'].strftime('%Y-%m-%d')
        
        # Buscar horários distintos para o dia
        cursor.execute("""
            SELECT DISTINCT TIME_FORMAT(Hora_Sessao, '%%H:%%i') as horario
            FROM Sessoes 
            WHERE Data_Sessao = %s
            ORDER BY Hora_Sessao ASC
        """, (data_sessao,))
        
        resultado = cursor.fetchall()
        
        # Extrair apenas os horários
        horarios = [horario[0] for horario in resultado]
        
        return horarios
        
    except Error as e:
        print("Erro ao listar horários disponíveis:", e)
        return []
    finally:
        con.close()

def listar_tipos_disponiveis_por_filme_dia_horario(id_filme, dia_info, horario):
    """
    Lista os tipos de sessão (dublado/legendado) disponíveis para um filme específico
    em um dia e horário específicos
    
    Args:
        id_filme: ID do filme
        dia_info: dict com informações do dia
        horario: string no formato 'HH:MM'
    
    Returns:
        Lista de tipos disponíveis
    """
    con = conectar()
    if con is None: 
        return []
    
    try:
        cursor = con.cursor()
        
        # Converter a data para o formato do banco
        data_sessao = dia_info['data'].strftime('%Y-%m-%d')
        
        # Buscar tipos distintos para o filme, dia e horário
        cursor.execute("""
            SELECT DISTINCT Tipo_Sessao
            FROM Sessoes 
            WHERE ID_Filme = %s 
            AND Data_Sessao = %s
            AND TIME_FORMAT(Hora_Sessao, '%%H:%%i') = %s
            ORDER BY Tipo_Sessao
        """, (id_filme, data_sessao, horario))
        
        resultado = cursor.fetchall()
        
        # Extrair apenas os tipos
        tipos = [tipo[0] for tipo in resultado]
        
        return tipos
        
    except Error as e:
        print("Erro ao listar tipos disponíveis:", e)
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

def obter_detalhes_sessao_completo(id_sessao):
    """
    Obtém todos os detalhes de uma sessão específica, incluindo informações do filme e sala
    
    Args:
        id_sessao: ID da sessão
    
    Returns:
        Dict com informações completas da sessão
    """
    con = conectar()
    if con is None: 
        return None
    
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                s.ID_Filme,
                s.ID_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                f.Titulo_Filme,
                f.Genero,
                f.Duracao,
                f.Classificacao,
                f.Cartaz_Path,
                f.Direcao,
                f.Sinopse,
                sa.Nome_Sala,
                sa.Capacidade
            FROM Sessoes s
            INNER JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Sessao = %s
        """, (id_sessao,))
        
        sessao = cursor.fetchone()
        
        if sessao:
            # Formatar hora
            hora = sessao['Hora_Sessao']
            if hasattr(hora, 'total_seconds'):
                total_seconds = int(hora.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                sessao['Hora_Formatada'] = f"{hours:02d}:{minutes:02d}"
            elif hasattr(hora, 'strftime'):
                sessao['Hora_Formatada'] = hora.strftime("%H:%M")
            else:
                sessao['Hora_Formatada'] = str(hora)
        
        return sessao
        
    except Error as e:
        print("Erro ao obter detalhes da sessão:", e)
        return None
    finally:
        con.close()

def verificar_lugares_disponiveis(id_sessao):
    """
    Verifica quantos lugares estão disponíveis para uma sessão
    
    Args:
        id_sessao: ID da sessão
    
    Returns:
        Número de lugares disponíveis
    """
    con = conectar()
    if con is None: 
        return 0
    
    try:
        cursor = con.cursor()
        
        # Buscar capacidade da sala e ingressos vendidos
        cursor.execute("""
            SELECT 
                sa.Capacidade,
                COUNT(i.ID_Ingresso) as ingressos_vendidos
            FROM Sessoes s
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            LEFT JOIN Ingressos i ON s.ID_Sessao = i.ID_Sessao
            WHERE s.ID_Sessao = %s
            GROUP BY sa.Capacidade
        """, (id_sessao,))
        
        resultado = cursor.fetchone()
        
        if resultado:
            capacidade = resultado[0]
            ingressos_vendidos = resultado[1] if resultado[1] else 0
            return capacidade - ingressos_vendidos
        else:
            return 0
            
    except Error as e:
        print("Erro ao verificar lugares disponíveis:", e)
        return 0
    finally:
        con.close()

def inserir_sessao(id_filme, id_sala, data_sessao, hora_sessao, tipo_sessao):
    """
    Insere uma nova sessão no banco de dados
    
    Args:
        id_filme: ID do filme
        id_sala: ID da sala
        data_sessao: Data da sessão (formato YYYY-MM-DD)
        hora_sessao: Hora da sessão (formato HH:MM)
        tipo_sessao: Tipo da sessão ('dublado' ou 'legendado')
    
    Returns:
        ID da sessão criada ou False se erro
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            INSERT INTO Sessoes (ID_Filme, ID_Sala, Data_Sessao, Hora_Sessao, Tipo_Sessao) 
            VALUES (%s, %s, %s, %s, %s)
        """, (id_filme, id_sala, data_sessao, hora_sessao, tipo_sessao))
        con.commit()
        return cursor.lastrowid
    except Error as e:
        print("Erro ao inserir sessão:", e)
        return False
    finally:
        con.close()

def editar_sessao(id_sessao, id_filme, id_sala, data_sessao, hora_sessao, tipo_sessao):
    """
    Edita uma sessão existente
    
    Args:
        id_sessao: ID da sessão a ser editada
        id_filme: ID do filme
        id_sala: ID da sala
        data_sessao: Data da sessão (formato YYYY-MM-DD)
        hora_sessao: Hora da sessão (formato HH:MM)
        tipo_sessao: Tipo da sessão ('dublado' ou 'legendado')
    
    Returns:
        True se sucesso, False se erro
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("""
            UPDATE Sessoes 
            SET ID_Filme=%s, ID_Sala=%s, Data_Sessao=%s, Hora_Sessao=%s, Tipo_Sessao=%s 
            WHERE ID_Sessao=%s
        """, (id_filme, id_sala, data_sessao, hora_sessao, tipo_sessao, id_sessao))
        con.commit()
        return True
    except Error as e:
        print("Erro ao editar sessão:", e)
        return False
    finally:
        con.close()

def excluir_sessao(id_sessao):
    """
    Exclui uma sessão do banco de dados
    
    Args:
        id_sessao: ID da sessão a ser excluída
    
    Returns:
        True se sucesso, False se erro
    """
    con = conectar()
    if con is None: 
        return False
    try:
        cursor = con.cursor()
        cursor.execute("DELETE FROM Sessoes WHERE ID_Sessao=%s", (id_sessao,))
        con.commit()
        return True
    except Error as e:
        print("Erro ao excluir sessão:", e)
        return False
    finally:
        con.close()

def buscar_sessao_por_id(id_sessao):
    """
    Busca uma sessão específica por ID
    
    Args:
        id_sessao: ID da sessão
    
    Returns:
        Dict com dados da sessão ou None se não encontrada
    """
    con = conectar()
    if con is None: 
        return None
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                s.ID_Filme,
                s.ID_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                f.Titulo_Filme,
                sa.Nome_Sala
            FROM Sessoes s
            INNER JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            WHERE s.ID_Sessao=%s
        """, (id_sessao,))
        resultado = cursor.fetchone()
        return resultado
    except Error as e:
        print("Erro ao buscar sessão:", e)
        return None
    finally:
        con.close()

def listar_todas_sessoes():
    """
    Lista todas as sessões com informações completas
    
    Returns:
        Lista de dicionários com dados das sessões
    """
    con = conectar()
    if con is None: 
        return []
    try:
        cursor = con.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.ID_Sessao,
                s.ID_Filme,
                s.ID_Sala,
                s.Data_Sessao,
                s.Hora_Sessao,
                s.Tipo_Sessao,
                f.Titulo_Filme,
                sa.Nome_Sala
            FROM Sessoes s
            INNER JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            INNER JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            ORDER BY s.Data_Sessao ASC, s.Hora_Sessao ASC
        """)
        resultado = cursor.fetchall()
        
        # Formatar horas
        for sessao in resultado:
            hora = sessao['Hora_Sessao']
            if hasattr(hora, 'total_seconds'):
                total_seconds = int(hora.total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                sessao['Hora_Formatada'] = f"{hours:02d}:{minutes:02d}"
            elif hasattr(hora, 'strftime'):
                sessao['Hora_Formatada'] = hora.strftime("%H:%M")
            else:
                sessao['Hora_Formatada'] = str(hora)
        
        return resultado
    except Error as e:
        print("Erro ao listar todas as sessões:", e)
        return []
    finally:
        con.close()