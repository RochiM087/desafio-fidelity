# Desafio Fidelity

Este repositório contém a solução para o desafio técnico da **Fidelity Pesquisas Cadastrais**.

## 📌 Objetivo

Refatorar e organizar um sistema de automação com Selenium que realiza consultas judiciais em plataformas de tribunais, utilizando uma base de dados em **PostgreSQL** conforme o modelo relacional fornecido.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Selenium
- PostgreSQL (psycopg2)
- tqdm

---

## 📁 Estrutura do Projeto

```
desafio-fidelity/
├── main.py
├── database.py
├── web_scraper.py
├── utils.py
├── schema.sql
├── requirements.txt
└── README.md
```

---

## ⚙️ Como Executar

1. Instale os pacotes:
```bash
pip install -r requirements.txt
```

2. Execute o programa com:
```bash
python main.py
```

3. Para usar um filtro específico:
```bash
python main.py --filtro 1
```

---

## 🗃️ Banco de Dados

O script `schema.sql` define a estrutura para PostgreSQL.
Crie o banco e execute o script com:

```bash
psql -U seu_usuario -d seu_banco -f schema.sql
```

---

## 🔧 Melhorias Aplicadas

- Modularização do código
- Separação de responsabilidades (DB, Selenium, lógica)
- Uso de boas práticas Python
- Adaptação total para PostgreSQL
- Tratamento de erros e controle de tentativas

---

## 📬 Entrega

Envie o link deste repositório público para:
- 📧 daniel_duperron@hotmail.com
- 📧 pedro.chaves@fidelitypesquisas.com.br

---

## ✅ Autor

Desenvolvido por Bruno Henrique da Rocha Rodrigues.