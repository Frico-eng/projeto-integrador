SET @id_atual = (SELECT COALESCE(MAX(ID_Ingresso), 0) FROM ingressos);
SET @data_inicio = '2025-01-01';
SET @data_fim = '2026-12-31';
SET @max_sessoes = (SELECT MAX(ID_Sessao) FROM sessoes);
SET @max_clientes = (SELECT MAX(ID_Usuario) FROM usuarios);

-- Inserir ingressos para todos os meses do ano (2025)
INSERT INTO ingressos (ID_Sessao, ID_Cliente, ID_Assento_Sessao, Valor, Data_Compra)
SELECT 
    -- Distribuir sessões uniformemente (todas as sessões disponíveis)
    FLOOR(1 + (RAND() * (@max_sessoes - 0.000001))),
    
    -- Clientes existentes
    FLOOR(1 + (RAND() * (@max_clientes - 0.000001))),
    
    -- Assentos disponíveis (relação com ID_Sessao)
    FLOOR(1 + (RAND() * 456)),
    
    -- Valor variável com base no tipo de sessão
    CASE 
        WHEN RAND() < 0.3 THEN 25.00  
        WHEN RAND() < 0.6 THEN 35.00 
        ELSE 45.00                    
    END,
    
    -- Data de compra distribuída ao longo de todos os meses de 2025
    TIMESTAMP(
        DATE_ADD(@data_inicio, INTERVAL FLOOR(RAND() * DATEDIFF(@data_fim, @data_inicio)) DAY),
        MAKETIME(
            FLOOR(8 + RAND() * 16),           -- Hora entre 08:00 e 23:59
            FLOOR(RAND() * 60),               -- Minuto aleatório
            FLOOR(RAND() * 60)                -- Segundo aleatório
        )
    )
FROM (
    -- Gerar sequência de números para criar múltiplos ingressos
    SELECT a.n + b.n*10 + c.n*100 + d.n*1000 + 1 as seq
    FROM 
        (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
         UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
         UNION ALL SELECT 8 UNION ALL SELECT 9) a,
        (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
         UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
         UNION ALL SELECT 8 UNION ALL SELECT 9) b,
        (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 
         UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 
         UNION ALL SELECT 8 UNION ALL SELECT 9) c,
        (SELECT 0 AS n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3) d
) numbers
WHERE seq <= 5000;
