from crud.crud_ingressos import processar_compra_ingressos, obter_ingresso_por_id


def main():
    id_cliente = 1
    id_sessao = 1
    lista_assentos = [1]
    valor_unitario = 25.00

    print("Iniciando teste de inserção de ingresso...")

    try:
        success, ids, msg = processar_compra_ingressos(id_cliente, id_sessao, lista_assentos, valor_unitario)
        print("Success:", success)
        print("IDs:", ids)
        print("Mensagem:", msg)

        if success and ids:
            ingresso = obter_ingresso_por_id(ids[0])
            print("Registro no DB:", ingresso)
    except Exception as e:
        print("Erro ao executar o teste:", e)


if __name__ == '__main__':
    main()
