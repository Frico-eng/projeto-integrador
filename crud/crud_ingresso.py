from conexao import conectar

def inserir_ingresso(id_sessao, id_cliente, assento, valor):
    con = conectar()
    if con is None:
        return False
    cursor = con.cursor()
    comando = """
        INSERT INTO ingressos (id_sessao, id_cliente, assento, valor, data_compra)
        VALUES (%s, %s, %s, %s, NOW())
    """
    cursor.execute(comando, (id_sessao, id_cliente, assento, valor))
    con.commit()
    con.close()
    return True

def listar_ingressos():
    con = conectar()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    comando = """
        SELECT 
            i.id_ingresso,
            f.titulo AS filme,
            s.nome_sala AS sala,
            se.data_sessao AS data,
            se.horario AS horario,
            i.assento,
            c.nome_cliente AS cliente,
            i.valor AS valor_pago,
            i.data_compra
        FROM ingressos i
        JOIN sessoes se ON i.id_sessao = se.id_sessao
        JOIN filmes f ON se.id_filme = f.id_filme
        JOIN salas s ON se.id_sala = s.id_sala
        JOIN clientes c ON i.id_cliente = c.id_cliente
        ORDER BY se.data_sessao DESC, se.horario ASC
    """
    cursor.execute(comando)
    resultado = cursor.fetchall()
    con.close()
    return resultado


def atualizar_ingresso(id_ingresso, id_sessao, id_cliente, assento, valor):
    con = conectar()
    if con is None:
        return False
    cursor = con.cursor()
    comando = """
        UPDATE ingressos
        SET id_sessao = %s,
            id_cliente = %s,
            assento = %s,
            valor = %s
        WHERE id_ingresso = %s
    """
    cursor.execute(comando, (id_sessao, id_cliente, assento, valor, id_ingresso))
    con.commit()
    con.close()
    return True

def excluir_ingresso(id_ingresso):
    con = conectar()
    if con is None:
        return False
    cursor = con.cursor()
    comando = "DELETE FROM ingressos WHERE id_ingresso = %s"
    cursor.execute(comando, (id_ingresso,))
    con.commit()
    con.close()
    return True
