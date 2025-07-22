import psycopg2

def conectar():
    return psycopg2.connect(
        host='10.0.270.18',
        user='usr_teste',
        password='teste',
        dbname='db_teste'
    )


def buscar_pesquisas(filtro, limite=210):
    con = conectar()
    cursor = con.cursor()

    cond = ''
    if filtro in [1, 3]:
        cond = ' AND rg <> "" '

    sql = f'''
        SELECT DISTINCT
            p.Cod_Cliente, p.Cod_Pesquisa, e.UF, p.Data_Entrada,
            COALESCE(p.nome_corrigido, p.nome) AS Nome, p.CPF,
            COALESCE(p.rg_corrigido, p.rg) AS RG, p.Nascimento,
            COALESCE(p.mae_corrigido, p.mae) AS Mae, p.anexo AS Anexo,
            ps.Resultado, ps.cod_spv_tipo
        FROM pesquisa p
        INNER JOIN servico s ON p.Cod_Servico = s.Cod_Servico
        LEFT JOIN lote_pesquisa lp ON p.Cod_Pesquisa = lp.Cod_Pesquisa
        LEFT JOIN lote l ON l.cod_lote = lp.cod_lote
        LEFT JOIN estado e ON e.Cod_UF = p.Cod_UF
        LEFT JOIN pesquisa_spv ps ON ps.Cod_Pesquisa = p.Cod_Pesquisa
            AND ps.Cod_SPV = 1 AND ps.filtro = {filtro}
        WHERE p.Data_Conclusao IS NULL
            AND ps.resultado IS NULL
            AND p.tipo = 0
            AND p.cpf <> "" {cond}
            AND (e.UF = "SP" OR p.Cod_UF_Nascimento = 26 OR p.Cod_UF_RG = 26)
        GROUP BY p.cod_pesquisa
        ORDER BY nome ASC, resultado DESC
        LIMIT {limite}
    '''

    cursor.execute(sql)
    resultados = cursor.fetchall()
    cursor.close()
    con.close()
    return resultados

def salvar_resultado(cod_pesquisa, resultado, filtro):
    sql = f'''
        INSERT INTO pesquisa_spv
        (Cod_Pesquisa, Cod_SPV, Cod_spv_computador, Cod_Spv_Tipo,
         Resultado, Cod_Funcionario, filtro, website_id)
        VALUES ({cod_pesquisa}, 1, 36, NULL, {resultado}, -1, {filtro}, 1)
    '''
    con = conectar()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
    con.close()
