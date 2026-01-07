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