WITH agregacao AS (
    SELECT 
        'Brasil' AS Localidade,
        COUNT(IDAtracacao) AS Numero_Atracacoes,
        AVG(TEsperaAtracacao) AS Tempo_Espera_Medio,
        AVG(TAtracado) AS Tempo_Atracado_Medio,
        Ano,
        Mes
    FROM atracacao_fato
    WHERE Ano BETWEEN 2021 AND 2023
    GROUP BY Ano, Mes
    UNION ALL
    SELECT 
        'Nordeste' AS Localidade,
        COUNT(IDAtracacao) AS Numero_Atracacoes,
        AVG(TEsperaAtracacao) AS Tempo_Espera_Medio,
        AVG(TAtracado) AS Tempo_Atracado_Medio,
        Ano,
        Mes
    FROM atracacao_fato
    WHERE UF IN ('MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA')
    AND Ano BETWEEN 2021 AND 2023
    GROUP BY Ano, Mes
    UNION ALL
    SELECT 
        'Ceará' AS Localidade,
        COUNT(IDAtracacao) AS Numero_Atracacoes,
        AVG(TEsperaAtracacao) AS Tempo_Espera_Medio,
        AVG(TAtracado) AS Tempo_Atracado_Medio,
        Ano,
        Mes
    FROM atracacao_fato
    WHERE UF = 'CE'
    AND Ano BETWEEN 2021 AND 2023
    GROUP BY Ano, Mes
)
SELECT 
    A.Localidade,
    A.Numero_Atracacoes,
    A.Tempo_Espera_Medio,
    A.Tempo_Atracado_Medio,
    A.Mes,
    A.Ano,
    COALESCE(
        ROUND(
            ((A.Numero_Atracacoes - B.Numero_Atracacoes) * 100.0 / NULLIF(B.Numero_Atracacoes, 0)), 2
        ), 0
    ) AS Variacao_Num_Atracacoes
FROM agregacao A
LEFT JOIN agregacao B 
    ON A.Localidade = B.Localidade
    AND A.Mes = B.Mes
    AND A.Ano = B.Ano + 1
ORDER BY A.Localidade, A.Ano, A.Mes;
