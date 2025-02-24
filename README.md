# **Engenharia de Dados - ANTAQ 🚢💾**

Este repositório contém os scripts de ETL desenvolvidos para manipulação e análise de dados do **Anuário Estatístico da ANTAQ**. O objetivo deste projeto é extrair, transformar e carregar os dados no **SQL Server**, garantindo que os analistas de BI e cientistas de dados possam acessá-los de maneira eficiente.

---

## **📌 Autoavaliação**
| Tópico | Nível (0-6) |
|--------|------------|
| Ferramentas de visualização de dados (Power BI, Qlik Sense e outros) | 6 |
| Manipulação e tratamento de dados com Python | 6 |
| Manipulação e tratamento de dados com PySpark | 4 |
| Desenvolvimento de data workflows em Ambiente Azure com Databricks | 3 |
| Desenvolvimento de data workflows com Airflow | 3 |
| Manipulação de bases de dados NoSQL | 4 |
| Web crawling e web scraping para mineração de dados | 6 |
| Construção de APIs: REST, SOAP e Microservices | 4 |

---

## (Questão 2a) Escolha da Estrutura de Dados (Data Lake, SQL Server ou NoSQL)

Para armazenar os dados do **Anuário Estatístico da ANTAQ**, analisamos três opções: **Data Lake, SQL Server e NoSQL (MongoDB)**.

### **📌 Escolha Final: Data Lake + SQL Server**

Optamos por um **modelo híbrido**, armazenando os dados no **Data Lake e SQL Server**.

---

### **📌 Justificativa para a Escolha**

1️⃣ **Data Lake** (Armazena os dados brutos e transformados antes do carregamento no SQL Server)
   - **Motivo**: Permite armazenar **dados estruturados e semi-estruturados** sem um esquema rígido.
   - **Benefícios**:
     ✅ Maior flexibilidade para processamento e transformação dos dados.  
     ✅ Suporte a múltiplos formatos (JSON, Parquet, CSV).  
     ✅ Facilita a reprocessamento e auditoria.  

2️⃣ **SQL Server** (Armazena os dados processados para consulta e análise no Power BI)
   - **Motivo**: Necessário para fornecer **dados estruturados e otimizados** para análises.  
   - **Benefícios**:
     ✅ Suporte a **transações e integridade referencial**.  
     ✅ Melhor desempenho para consultas complexas.  
     ✅ Integração nativa com **Power BI** (ferramenta dos analistas do cliente).  
   - **Uso no Projeto**:
     - Criamos as tabelas `atracacao_fato` e `carga_fato` no SQL Server.
     - Implementamos índices para otimizar consultas.

3️⃣ **NoSQL (MongoDB) – Não utilizado**  
   - **Motivo**: O banco relacional atende melhor aos requisitos do projeto.  
   - **Quando seria útil?** Para armazenar logs de eventos ou dados não estruturados.  

---

### **📌 Conclusão**
✅ **Os dados brutos e extraídos são armazenados no Data Lake.**  
✅ **Os dados processados são carregados no SQL Server para otimizar a análise no Power BI.**  
✅ **O NoSQL não foi utilizado, pois o SQL Server atende melhor às necessidades do projeto.**  

---
## (Questão 2b) •Criar os scripts SQL de criação das tabelas (atracacao_fato e carga_fato) e adicionar no repositório.
Os scripts SQL para a criação das tabelas atracacao_fato e carga_fato podem ser encontrados no seguinte arquivo:

### 📂 sql/criar_tabelas.sql

Este script cria a estrutura necessária no SQL Server para armazenar os dados processados no pipeline de ETL. As tabelas foram projetadas para armazenar informações sobre:

atracacao_fato 🚢

ID da atracação, porto, tipo de navegação, datas relevantes, tempo de espera e operação, entre outras informações.
carga_fato 📦

ID da carga, origem/destino, mercadoria transportada, tipo de operação, TEU, quantidade transportada e peso líquido da carga.
📌 Como utilizar?
Para criar as tabelas no banco de dados, basta executar o script no SQL Server utilizando um cliente como SQL Server Management Studio (SSMS) ou Azure Data Studio.

## (Questão 2c) •Criar a query otimizada para Excel que responde à Questão.
A consulta SQL otimizada para o Excel que fornece os dados solicitados sobre número de atracações, tempo de espera médio e tempo atracado médio pode ser encontrada no seguinte arquivo:

### 📂 sql/query_economistas.sql

📌 O que essa consulta faz?
Filtra os dados apenas para os anos 2021 a 2023.
Agrupa as informações por localidade (Ceará, Nordeste e Brasil) e mês/ano.
Calcula os seguintes indicadores:
Número de atracações no período.
Variação percentual do número de atracações em relação ao mesmo mês do ano anterior.
Tempo médio de espera para atracação.
Tempo médio que os navios ficaram atracados.
📌 Como utilizar no Excel?
Executar a query no SQL Server utilizando SQL Server Management Studio (SSMS) ou Azure Data Studio.
Exportar os resultados para CSV ou Excel diretamente no SQL Server.
Abrir o arquivo no Excel para análise e visualização dos dados.
💡 Essa consulta foi otimizada para minimizar o número de linhas, garantindo melhor desempenho ao abrir no Excel.

## (Questão 3) 🤖 .Criar a DAG do Airflow 

Para garantir a orquestração do ETL dos dados da ANTAQ, implementamos um ambiente utilizando **Apache Airflow** e **Docker**.

### 📂 **Arquivos principais**
- `docker/docker-compose.yml` → Configuração do ambiente Docker para Airflow.
- `airflow/dags/antaq_etl_dag.py` → DAG do Airflow que executa o pipeline ETL.
- `airflow/scripts/download_dados.py` → Script que baixa os dados da ANTAQ.
- `airflow/scripts/etl_pipeline.py` → Script que processa os dados e armazena no SQL Server.

### ⚙️ **Execução do Workflow**
O fluxo de trabalho do Airflow executa as seguintes etapas **a cada 15 dias**:
1️⃣ **Verificar se os dados estão disponíveis** no Data Lake antes do processamento.  
2️⃣ **Baixar os dados** da ANTAQ para o Data Lake.  
3️⃣ **Realizar a transformação dos dados** e inseri-los no SQL Server.  
4️⃣ **Enviar um e-mail de confirmação** ao final do processo.

### 🛠 **Como rodar o Airflow com Docker**
1. **Iniciar o ambiente**
   ```bash
   cd docker
   docker-compose up -d


## **📁 Estrutura do Repositório**
```bash
engenharia-de-dados-antaq/
│── airflow/                 # DAGs e scripts de ETL no Apache Airflow
│   ├── data/                # Diretório para armazenar dados baixados
│   ├── dags/                # Arquivos das DAGs do Airflow
│   ├── scripts/             # Scripts de ETL
│   ├── config/              # Arquivos de configuração
│── docker/                  # Configuração para rodar o projeto em contêineres
│── docs/                    # Documentação do projeto
│   ├── autoavaliacao.md      # Autoavaliação detalhada
│   ├── estrutura_dados.md    # Justificativa sobre armazenamento SQL/NoSQL/Data Lake
│── sql/                     # Scripts SQL para criação e manipulação de tabelas
│   ├── criar_tabelas.sql     # Script para criar tabelas no SQL Server
│   ├── inserir_dados_sql.py  # Script para inserir dados no banco de dados
│   ├── query_economistas.sql # Consulta SQL otimizada para economistas
│── .gitignore                # Arquivos que não devem ser versionados
│── README.md                 # Documentação principal do projeto
```

---

## **⚙️ Configuração do Ambiente**
### **1️⃣ Instalar dependências**
```bash
# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Instalar as bibliotecas necessárias
pip install -r requirements.txt
```

### **2️⃣ Criar as tabelas no SQL Server**
```bash
# Rodar o script para criar as tabelas necessárias
psql -U meu_usuario -d minha_base -f sql/criar_tabelas.sql
```

### **3️⃣ Executar o pipeline de ETL**
```bash
# Executar o script de ETL no Apache Airflow
python airflow/scripts/etl_pipeline.py
```

---

## **📊 Justificativa para Uso de Data Lake, SQL ou NoSQL**

Para a estruturação e armazenamento dos dados da ANTAQ, foi adotada uma abordagem híbrida, combinando Data Lake, SQL Server e NoSQL (MongoDB). Cada tecnologia foi escolhida estrategicamente para atender às necessidades de armazenamento, processamento e consulta dos dados, garantindo flexibilidade e eficiência.

### 1. Data Lake (Armazenamento Bruto)
Motivo: O Data Lake foi utilizado para armazenar os dados brutos extraídos da ANTAQ, garantindo que os cientistas de dados tenham acesso à informação completa para análises exploratórias e modelagens avançadas.
Benefícios:
Capacidade de armazenar grandes volumes de dados em diferentes formatos (estruturados, semiestruturados e não estruturados).
Permite análise retrospectiva dos dados sem perda de informações.
Facilita a reprocessamento de dados conforme necessário.
### 2. SQL Server (Dados Estruturados)
Motivo: O SQL Server foi escolhido para armazenar os dados já transformados e estruturados, garantindo alto desempenho para consultas analíticas realizadas por analistas e economistas.
Benefícios:
Facilita a indexação e otimização das consultas.
Garante integridade referencial e consistência dos dados.
Permite integração direta com ferramentas de BI, como Power BI.
### 3. NoSQL (MongoDB - Dados Semi-Estruturados)
Motivo: O MongoDB foi utilizado para armazenar metadados e logs relacionados às cargas, proporcionando maior flexibilidade para consultas dinâmicas e acesso rápido a informações não estruturadas.
Benefícios:
Melhor desempenho para armazenamento de documentos JSON (logs, status de processamento, metadados de cargas).
Flexibilidade para armazenar diferentes formatos de dados sem necessidade de um esquema rígido.
Facilidade na escalabilidade horizontal, permitindo crescimento eficiente.
### Conclusão

| Tipo de Armazenamento | Motivo |
|----------------------|--------|
| **Data Lake** | Armazena dados brutos para análises exploratórias. |
| **SQL Server** | Organiza os dados estruturados para consultas rápidas e eficientes. |
| **NoSQL (MongoDB)** | Melhor para armazenar dados semi-estruturados, como logs e metadados de carga. |

---

## **🚀 Executando com Docker e Apache Airflow**
Caso prefira rodar o projeto com **Docker e Airflow**, siga os passos abaixo:

### **1️⃣ Criar os contêineres**
```bash
docker-compose up -d
```

### **2️⃣ Acessar a interface do Airflow**
```bash
http://localhost:8080
```
- **Login:** admin
- **Senha:** admin

---

## **📈 Consultas SQL para Análise dos Economistas**
Os economistas precisam de uma consulta otimizada para exportar dados ao **Excel** sem sobrecarregar a ferramenta. O script SQL para esta análise está no arquivo [`sql/query_economistas.sql`](sql/query_economistas.sql).

---

## **✅ Conclusão**
Este projeto entrega um **pipeline de ETL completo** para ingestão, transformação e armazenamento dos dados do **Anuário Estatístico da ANTAQ**, utilizando **Python, Pyspark, SQL Server e Apache Airflow**.

**💡 Tecnologias utilizadas:**  
✅ **Python**  
✅ **PySpark**  
✅ **SQL Server**  
✅ **Apache Airflow**  
✅ **Docker**  
✅ **Power BI**  

Este repositório representa minha solução para o desafio de **Especialista em Engenharia de Dados do Observatório da Indústria**. 🚀💡

