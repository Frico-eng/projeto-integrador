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

def criar_ingresso(id_sessao, id_cliente, id_assento_sessao, valor):
    conexao = conectar()
    if conexao is None:
        return -1
    
    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT * FROM Ingressos 
            WHERE ID_Assento_Sessao = %s
        """, (id_assento_sessao,))
        
        if cursor.fetchone():
            print("Erro: Assento já está ocupado!")
            cursor.close()
            conexao.close()
            return -1

        cursor.execute("""
            INSERT INTO Ingressos 
            (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra) 
            VALUES (%s, %s, %s, %s, NOW())
        """, (id_sessao, id_cliente, id_assento_sessao, valor))
        
        conexao.commit()
        id_ingresso = cursor.lastrowid
        
        print(f"Ingresso criado com sucesso! ID: {id_ingresso}")
        
        cursor.close()
        conexao.close()
        
        return id_ingresso
        
    except Error as e:
        print("Erro ao criar ingresso:", e)
        if conexao:
            conexao.rollback()
            conexao.close()
        return -1

def criar_varios_ingressos(ingressos_data):
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor()
        ids_criados = []
        
        for ingresso in ingressos_data:
            id_sessao, id_cliente, id_assento_sessao, valor = ingresso
            
            # Verificar se o assento já está ocupado
            cursor.execute("""
                SELECT * FROM Ingressos 
                WHERE ID_Assento_Sessao = %s
            """, (id_assento_sessao,))
            
            if cursor.fetchone():
                print(f"Erro: Assento {id_assento_sessao} já está ocupado! Pulando...")
                continue
            
            # Inserir novo ingresso
            cursor.execute("""
                INSERT INTO Ingressos 
                (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra) 
                VALUES (%s, %s, %s, %s, NOW())
            """, (id_sessao, id_cliente, id_assento_sessao, valor))
            
            ids_criados.append(cursor.lastrowid)
        
        conexao.commit()
        print(f"{len(ids_criados)} ingressos criados com sucesso!")
        
        cursor.close()
        conexao.close()
        
        return ids_criados
        
    except Error as e:
        print("Erro ao criar vários ingressos:", e)
        if conexao:
            conexao.rollback()
            conexao.close()
        return []

def obter_ingresso_por_id(id_ingresso):
    conexao = conectar()
    if conexao is None:
        return None
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM Ingressos 
            WHERE ID_Ingresso = %s
        """, (id_ingresso,))
        
        ingresso = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        return ingresso
        
    except Error as e:
        print("Erro ao obter ingresso por ID:", e)
        if conexao:
            conexao.close()
        return None

def obter_ingressos_por_cliente(id_cliente):

    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT i.*, s.Hora_Sessao, f.Titulo_Filme, sa.Nome_Sala, 
                   a.Numero_Assento, a.Fileira_Assento
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE i.ID_Cliente = %s
            ORDER BY i.Data_Compra DESC
        """, (id_cliente,))
        
        ingressos = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return ingressos
        
    except Error as e:
        print("Erro ao obter ingressos por cliente:", e)
        if conexao:
            conexao.close()
        return []

def obter_ingressos_por_sessao(id_sessao):
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT i.*, u.Nome_Usuario, a.Numero_Assento, a.Fileira_Assento
            FROM Ingressos i
            JOIN Usuarios u ON i.ID_Cliente = u.ID_Usuario
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            WHERE i.ID_Sessao = %s
            ORDER BY a.Fileira_Assento, a.Numero_Assento
        """, (id_sessao,))
        
        ingressos = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return ingressos
        
    except Error as e:
        print("Erro ao obter ingressos por sessao:", e)
        if conexao:
            conexao.close()
        return []

def verificar_assento_disponivel(id_assento_sessao):
    conexao = conectar()
    if conexao is None:
        return False
    
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT ID_Ingresso FROM Ingressos 
            WHERE ID_Assento_Sessao = %s
        """, (id_assento_sessao,))
        
        resultado = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        return resultado is None  # Se não encontrou, está disponível
        
    except Error as e:
        print("Erro ao verificar assento:", e)
        if conexao:
            conexao.close()
        return False

def obter_ingressos_vendidos_sessao(id_sessao):
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor()
        
        cursor.execute("""
            SELECT i.ID_Assento_Sessao 
            FROM Ingressos i
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            WHERE ass.ID_Sessao = %s
        """, (id_sessao,))
        
        assentos_vendidos = [row[0] for row in cursor.fetchall()]
        
        cursor.close()
        conexao.close()
        
        return assentos_vendidos
        
    except Error as e:
        print("Erro ao obter assentos vendidos:", e)
        if conexao:
            conexao.close()
        return []

def cancelar_ingresso(id_ingresso):
    conexao = conectar()
    if conexao is None:
        return False
    
    try:
        cursor = conexao.cursor()
        
        # Verificar se o ingresso existe
        cursor.execute("""
            SELECT * FROM Ingressos WHERE ID_Ingresso = %s
        """, (id_ingresso,))
        
        if not cursor.fetchone():
            print("Erro: Ingresso não encontrado!")
            cursor.close()
            conexao.close()
            return False
        
        # Excluir ingresso
        cursor.execute("""
            DELETE FROM Ingressos WHERE ID_Ingresso = %s
        """, (id_ingresso,))
        
        conexao.commit()
        print(f"Ingresso {id_ingresso} cancelado com sucesso!")
        
        cursor.close()
        conexao.close()
        
        return True
        
    except Error as e:
        print("Erro ao cancelar ingresso:", e)
        if conexao:
            conexao.rollback()
            conexao.close()
        return False

def obter_relatorio_vendas(data_inicio=None, data_fim=None):
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        query = """
            SELECT 
                DATE(i.Data_Compra) as Data,
                COUNT(*) as Total_Ingressos,
                SUM(i.Valor) as Total_Valor,
                f.Titulo_Filme as Filme_Mais_Vendido,
                COUNT(DISTINCT i.ID_Cliente) as Total_Clientes
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
        """
        
        params = []
        
        if data_inicio and data_fim:
            query += " WHERE DATE(i.Data_Compra) BETWEEN %s AND %s"
            params.extend([data_inicio, data_fim])
        elif data_inicio:
            query += " WHERE DATE(i.Data_Compra) >= %s"
            params.append(data_inicio)
        elif data_fim:
            query += " WHERE DATE(i.Data_Compra) <= %s"
            params.append(data_fim)
        
        query += """
            GROUP BY DATE(i.Data_Compra), f.Titulo_Filme
            ORDER BY Data DESC, Total_Valor DESC
        """
        
        cursor.execute(query, params)
        relatorio = cursor.fetchall()
        
        cursor.close()
        conexao.close()
        
        return relatorio
        
    except Error as e:
        print("Erro ao obter relatório de vendas:", e)
        if conexao:
            conexao.close()
        return []

# ============ FUNÇÕES PARA INTEGRAÇÃO COM O SISTEMA ============

def processar_compra_ingressos(id_cliente, id_sessao, lista_assentos_ids, valor_unitario):
    if not lista_assentos_ids:
        return False, [], "Nenhum assento selecionado!"
    
    # Preparar dados para inserção múltipla
    ingressos_data = []
    for id_assento_sessao in lista_assentos_ids:
        # Verificar se o assento está disponível
        if not verificar_assento_disponivel(id_assento_sessao):
            return False, [], f"Assento {id_assento_sessao} já está ocupado!"
        
        ingressos_data.append((id_sessao, id_cliente, id_assento_sessao, valor_unitario))
    
    # Criar ingressos
    ids_ingressos = criar_varios_ingressos(ingressos_data)
    
    if ids_ingressos:
        total = len(ids_ingressos) * valor_unitario
        mensagem = f"Compra realizada com sucesso!\n{len(ids_ingressos)} ingressos criados.\nTotal: R$ {total:.2f}"
        return True, ids_ingressos, mensagem
    else:
        return False, [], "Erro ao processar a compra!"

def obter_detalhes_ingresso_completo(id_ingresso):
    conexao = conectar()
    if conexao is None:
        return None
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                i.ID_Ingresso,
                i.Valor,
                i.Data_Compra,
                s.Hora_Sessao,
                s.Data_Sessao,
                f.Titulo_Filme,
                f.Duracao,
                f.Classificacao,
                f.Genero,
                sa.Nome_Sala,
                sa.Tipo_Tela,
                sa.Tipo_Som,
                a.Numero_Assento,
                a.Fileira_Assento,
                a.Tipo_Assento,
                u.Nome_Usuario,
                u.Email
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            JOIN Assentos_Sessao ass ON i.ID_Assento_Sessao = ass.ID_Assento_Sessao
            JOIN Assentos a ON ass.ID_Assento = a.ID_Assento
            JOIN Usuarios u ON i.ID_Cliente = u.ID_Usuario
            WHERE i.ID_Ingresso = %s
        """, (id_ingresso,))
        
        detalhes = cursor.fetchone()
        
        cursor.close()
        conexao.close()
        
        return detalhes
        
    except Error as e:
        print("Erro ao obter detalhes do ingresso:", e)
        if conexao:
            conexao.close()
        return None

# ============ FUNÇÕES PARA RELATÓRIOS ============

def obter_vendas_por_filme(periodo="mensal"):
    """Retorna vendas agrupadas por filme para o período especificado"""
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Definir período baseado no parâmetro
        if periodo == "diário":
            date_filter = "DATE(i.Data_Compra) = CURDATE()"
        elif periodo == "mensal":
            date_filter = "MONTH(i.Data_Compra) = MONTH(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "quatrenal":
            date_filter = "QUARTER(i.Data_Compra) = QUARTER(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "anual":
            date_filter = "YEAR(i.Data_Compra) = YEAR(CURDATE())"
        else:
            date_filter = "1=1"  # Todos os registros
        
        cursor.execute(f"""
            SELECT 
                f.Titulo_Filme,
                COUNT(i.ID_Ingresso) as total_ingressos,
                COALESCE(SUM(i.Valor), 0) as faturamento_total,
                COALESCE(AVG(i.Valor), 0) as preco_medio
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            WHERE {date_filter}
            GROUP BY f.ID_Filme, f.Titulo_Filme
            ORDER BY total_ingressos DESC
        """)
        
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        
        return resultados
        
    except Error as e:
        print("Erro ao obter vendas por filme:", e)
        if conexao:
            conexao.close()
        return []

def obter_faturamento_por_periodo(periodo="mensal"):
    """Retorna faturamento agrupado por período"""
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        if periodo == "diário":
            group_by = "DATE(i.Data_Compra)"
            select_date = "DATE(i.Data_Compra) as periodo"
        elif periodo == "mensal":
            group_by = "DATE_FORMAT(i.Data_Compra, '%Y-%m')"
            select_date = "DATE_FORMAT(i.Data_Compra, '%Y-%m') as periodo"
        elif periodo == "quatrenal":
            group_by = "CONCAT(YEAR(i.Data_Compra), '-Q', QUARTER(i.Data_Compra))"
            select_date = "CONCAT(YEAR(i.Data_Compra), '-Q', QUARTER(i.Data_Compra)) as periodo"
        elif periodo == "anual":
            group_by = "YEAR(i.Data_Compra)"
            select_date = "YEAR(i.Data_Compra) as periodo"
        else:
            group_by = "DATE(i.Data_Compra)"
            select_date = "DATE(i.Data_Compra) as periodo"
        
        cursor.execute(f"""
            SELECT 
                {select_date},
                COUNT(i.ID_Ingresso) as total_ingressos,
                COALESCE(SUM(i.Valor), 0) as faturamento_total,
                COALESCE(AVG(i.Valor), 0) as preco_medio
            FROM Ingressos i
            GROUP BY {group_by}
            ORDER BY {group_by} DESC
            LIMIT 30
        """)
        
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        
        return resultados
        
    except Error as e:
        print("Erro ao obter faturamento por período:", e)
        if conexao:
            conexao.close()
        return []

def obter_ingressos_por_sessao(periodo="mensal"):
    """Retorna ingressos vendidos por sessão"""
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Definir período baseado no parâmetro
        if periodo == "diário":
            date_filter = "DATE(i.Data_Compra) = CURDATE()"
        elif periodo == "mensal":
            date_filter = "MONTH(i.Data_Compra) = MONTH(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "quatrenal":
            date_filter = "QUARTER(i.Data_Compra) = QUARTER(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "anual":
            date_filter = "YEAR(i.Data_Compra) = YEAR(CURDATE())"
        else:
            date_filter = "1=1"
        
        cursor.execute(f"""
            SELECT 
                f.Titulo_Filme,
                s.Data_Sessao,
                s.Hora_Sessao,
                sa.Nome_Sala,
                COUNT(i.ID_Ingresso) as ingressos_vendidos,
                (SELECT COUNT(*) FROM Assentos_Sessao ass WHERE ass.ID_Sessao = s.ID_Sessao) as capacidade_total,
                COALESCE(SUM(i.Valor), 0) as faturamento_sessao
            FROM Sessoes s
            LEFT JOIN Ingressos i ON s.ID_Sessao = i.ID_Sessao AND {date_filter}
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            JOIN Salas sa ON s.ID_Sala = sa.ID_Sala
            GROUP BY s.ID_Sessao, f.Titulo_Filme, s.Data_Sessao, s.Hora_Sessao, sa.Nome_Sala
            ORDER BY s.Data_Sessao DESC, s.Hora_Sessao DESC
            LIMIT 50
        """)
        
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        
        return resultados
        
    except Error as e:
        print("Erro ao obter ingressos por sessão:", e)
        if conexao:
            conexao.close()
        return []

def obter_filmes_mais_populares(periodo="mensal", limite=10):
    """Retorna os filmes mais populares baseado em ingressos vendidos"""
    conexao = conectar()
    if conexao is None:
        return []
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Definir período baseado no parâmetro
        if periodo == "diário":
            date_filter = "DATE(i.Data_Compra) = CURDATE()"
        elif periodo == "mensal":
            date_filter = "MONTH(i.Data_Compra) = MONTH(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "quatrenal":
            date_filter = "QUARTER(i.Data_Compra) = QUARTER(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "anual":
            date_filter = "YEAR(i.Data_Compra) = YEAR(CURDATE())"
        else:
            date_filter = "1=1"
        
        cursor.execute(f"""
            SELECT 
                f.Titulo_Filme,
                f.Genero,
                f.Classificacao,
                COUNT(i.ID_Ingresso) as total_ingressos,
                COALESCE(SUM(i.Valor), 0) as faturamento_total,
                COALESCE(AVG(i.Valor), 0) as preco_medio,
                COUNT(DISTINCT s.ID_Sessao) as sessoes_realizadas
            FROM Filmes f
            LEFT JOIN Sessoes s ON f.ID_Filme = s.ID_Filme
            LEFT JOIN Ingressos i ON s.ID_Sessao = i.ID_Sessao AND {date_filter}
            GROUP BY f.ID_Filme, f.Titulo_Filme, f.Genero, f.Classificacao
            ORDER BY total_ingressos DESC
            LIMIT {limite}
        """)
        
        resultados = cursor.fetchall()
        cursor.close()
        conexao.close()
        
        return resultados
        
    except Error as e:
        print("Erro ao obter filmes mais populares:", e)
        if conexao:
            conexao.close()
        return []

def obter_estatisticas_gerais(periodo="mensal"):
    """Retorna estatísticas gerais do cinema"""
    conexao = conectar()
    if conexao is None:
        return {}
    
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Definir período baseado no parâmetro
        if periodo == "diário":
            date_filter = "DATE(i.Data_Compra) = CURDATE()"
        elif periodo == "mensal":
            date_filter = "MONTH(i.Data_Compra) = MONTH(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "quatrenal":
            date_filter = "QUARTER(i.Data_Compra) = QUARTER(CURDATE()) AND YEAR(i.Data_Compra) = YEAR(CURDATE())"
        elif periodo == "anual":
            date_filter = "YEAR(i.Data_Compra) = YEAR(CURDATE())"
        else:
            date_filter = "1=1"
        
        # Estatísticas gerais
        cursor.execute(f"""
            SELECT 
                COUNT(DISTINCT i.ID_Ingresso) as total_ingressos_vendidos,
                COALESCE(SUM(i.Valor), 0) as faturamento_total,
                COALESCE(AVG(i.Valor), 0) as preco_medio_ingresso,
                COUNT(DISTINCT i.ID_Cliente) as total_clientes_unicos,
                COUNT(DISTINCT s.ID_Sessao) as total_sessoes_realizadas
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            WHERE {date_filter}
        """)
        
        estatisticas = cursor.fetchone() or {}
        
        # Filme mais vendido
        cursor.execute(f"""
            SELECT f.Titulo_Filme, COUNT(i.ID_Ingresso) as ingressos
            FROM Ingressos i
            JOIN Sessoes s ON i.ID_Sessao = s.ID_Sessao
            JOIN Filmes f ON s.ID_Filme = f.ID_Filme
            WHERE {date_filter}
            GROUP BY f.ID_Filme, f.Titulo_Filme
            ORDER BY ingressos DESC
            LIMIT 1
        """)
        
        filme_mais_vendido = cursor.fetchone()
        if filme_mais_vendido:
            estatisticas['filme_mais_vendido'] = filme_mais_vendido['Titulo_Filme']
            estatisticas['ingressos_filme_mais_vendido'] = filme_mais_vendido['ingressos']
        
        cursor.close()
        conexao.close()
        
        return estatisticas
        
    except Error as e:
        print("Erro ao obter estatísticas gerais:", e)
        if conexao:
            conexao.close()
        return {}

# ============ TESTES ============
if __name__ == "__main__":
    # Teste das funções
    print("Testando CRUD de ingressos...")
    
    # Testar conexão
    print("1. Testando conexão...")
    conn = conectar()
    if conn:
        print("✓ Conexão OK")
        conn.close()
    else:
        print("✗ Falha na conexão")
    
    # Testar criação de ingresso
    print("\n2. Testando criação de ingresso...")
    id_teste = criar_ingresso(
        id_sessao=1,
        id_cliente=1,
        id_assento_sessao=1,
        valor=25.00
    )
    
    if id_teste != -1:
        print(f"✓ Ingresso criado com ID: {id_teste}")
        
        # Testar obtenção
        print("\n3. Testando obtenção por ID...")
        ingresso = obter_ingresso_por_id(id_teste)
        if ingresso:
            print(f"✓ Ingresso encontrado: {ingresso}")
        
        # Testar cancelamento
        print("\n4. Testando cancelamento...")
        if cancelar_ingresso(id_teste):
            print("✓ Ingresso cancelado com sucesso")
    else:
        print("✗ Falha ao criar ingresso")
    
    print("\nTeste concluído!")