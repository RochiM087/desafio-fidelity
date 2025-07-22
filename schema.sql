-- Tabela estado
CREATE TABLE estado (
    cod_uf INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    uf VARCHAR(2) NOT NULL,
    cod_fornecedor INTEGER,
    nome VARCHAR(255)
);

-- Tabela lote
CREATE TABLE lote (
    cod_lote INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cod_lote_prazo INTEGER,
    data_criacao DATE,
    cod_funcionario INTEGER,
    tipo INTEGER,
    prioridade INTEGER
);

-- Tabela lote_pesquisa
CREATE TABLE lote_pesquisa (
    cod_lote_pesquisa INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cod_lote INTEGER REFERENCES lote(cod_lote),
    cod_pesquisa INTEGER,
    cod_funcionario INTEGER,
    cod_funcionario_conclusao INTEGER,
    cod_fornecedor INTEGER,
    data_entrada DATE,
    data_conclusao DATE,
    cod_uf INTEGER REFERENCES estado(cod_uf),
    obs TEXT
);

-- Tabela servico
CREATE TABLE servico (
    cod_servico INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    civil BOOLEAN,
    criminal BOOLEAN
);

-- Tabela pesquisa
CREATE TABLE pesquisa (
    cod_pesquisa INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cod_cliente INTEGER,
    cod_uf INTEGER REFERENCES estado(cod_uf),
    cod_servico INTEGER REFERENCES servico(cod_servico),
    tipo INTEGER,
    cpf VARCHAR(14),
    cod_uf_nascimento INTEGER,
    cod_uf_rg INTEGER,
    data_entrada DATE,
    data_conclusao DATE,
    nome VARCHAR(255),
    nome_corrigido VARCHAR(255),
    rg VARCHAR(20),
    rg_corrigido VARCHAR(20),
    nascimento DATE,
    mae VARCHAR(255),
    mae_corrigido VARCHAR(255),
    anexo TEXT
);

-- Tabela pesquisa_spv
CREATE TABLE pesquisa_spv (
    cod_pesquisa INTEGER REFERENCES pesquisa(cod_pesquisa),
    cod_spv INTEGER,
    cod_spv_computador INTEGER,
    cod_spv_tipo INTEGER,
    cod_funcionario INTEGER,
    filtro INTEGER,
    website_id INTEGER,
    resultado INTEGER,
    PRIMARY KEY (cod_pesquisa, cod_spv, filtro)
);