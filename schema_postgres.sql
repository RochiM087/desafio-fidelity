CREATE TABLE estado (
    Cod_UF SERIAL PRIMARY KEY,
    UF VARCHAR(2) NOT NULL
);

CREATE TABLE servico (
    Cod_Servico SERIAL PRIMARY KEY,
    Nome_Servico VARCHAR(255)
);

CREATE TABLE lote (
    cod_lote SERIAL PRIMARY KEY,
    descricao TEXT
);

CREATE TABLE lote_pesquisa (
    id SERIAL PRIMARY KEY,
    Cod_Pesquisa INT NOT NULL,
    cod_lote INT,
    FOREIGN KEY (cod_lote) REFERENCES lote (cod_lote)
);

CREATE TABLE pesquisa (
    Cod_Pesquisa SERIAL PRIMARY KEY,
    Cod_Cliente INT,
    Cod_Servico INT,
    Cod_UF INT,
    Cod_UF_Nascimento INT,
    Cod_UF_RG INT,
    nome VARCHAR(255),
    nome_corrigido VARCHAR(255),
    CPF VARCHAR(20),
    rg VARCHAR(50),
    rg_corrigido VARCHAR(50),
    Nascimento DATE,
    mae VARCHAR(255),
    mae_corrigido VARCHAR(255),
    tipo INT,
    Data_Entrada TIMESTAMP,
    Data_Conclusao TIMESTAMP,
    anexo TEXT,
    FOREIGN KEY (Cod_Servico) REFERENCES servico (Cod_Servico),
    FOREIGN KEY (Cod_UF) REFERENCES estado (Cod_UF)
);

CREATE TABLE pesquisa_spv (
    id SERIAL PRIMARY KEY,
    Cod_Pesquisa INT NOT NULL,
    Cod_SPV INT NOT NULL,
    Cod_spv_computador INT NOT NULL,
    Cod_Spv_Tipo INT,
    Resultado INT,
    Cod_Funcionario INT,
    filtro INT,
    website_id INT,
    FOREIGN KEY (Cod_Pesquisa) REFERENCES pesquisa (Cod_Pesquisa)
);
