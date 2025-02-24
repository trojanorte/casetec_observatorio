-- Remover as tabelas se já existirem antes de criá-las novamente
DROP TABLE IF EXISTS carga_fato CASCADE;
DROP TABLE IF EXISTS atracacao_fato CASCADE;

-- Criar a tabela atracacao_fato
CREATE TABLE atracacao_fato (
    IDAtracacao INT PRIMARY KEY,
    CDTUP VARCHAR(50),
    IDBerco INT,
    Berco VARCHAR(100),
    PortoAtracacao VARCHAR(100),
    Municipio VARCHAR(100),
    ApelidoInstalacaoPortuaria VARCHAR(100),
    UF CHAR(2),
    ComplexoPortuario VARCHAR(100),
    SGUF CHAR(2),
    TipoAutoridadePortuaria VARCHAR(100),
    RegiaoGeografica VARCHAR(100),
    DataAtracacao DATE,
    DataChegada DATE,
    DataDesatracacao DATE,
    DataInicioOperacao DATE,
    DataTerminoOperacao DATE,
    AnoInicioOperacao INT,
    MesInicioOperacao INT,
    TipoOperacao VARCHAR(50),
    TEsperaAtracacao FLOAT,
    TEsperaInicioOp FLOAT,
    TOperacao FLOAT,
    TEsperaDesatracacao FLOAT,
    TAtracado FLOAT,
    TEstadia FLOAT
);

-- Criar a tabela carga_fato
CREATE TABLE carga_fato (
    IDCarga INT PRIMARY KEY,
    IDAtracacao INT,
    Origem VARCHAR(100),
    Destino VARCHAR(100),
    CDMercadoria VARCHAR(50),
    STNaturezaCarga VARCHAR(50),
    TipoOperacaoCarga VARCHAR(50),
    CargaGeralAcondicionamento VARCHAR(50),
    Sentido VARCHAR(50),
    TipoNavegacao VARCHAR(50),
    TEU INT,
    FlagAutorizacao BOOLEAN,
    QTCarga FLOAT,
    FlagCabotagem BOOLEAN,
    VLPesoCargaBruta FLOAT,
    FlagCabotagemMovimentacao BOOLEAN,
    AnoInicioOperacao INT,
    FlagConteinerTamanho BOOLEAN,
    MesInicioOperacao INT,
    FlagLongoCurso BOOLEAN,
    PortoAtracacao VARCHAR(100),
    SGUF CHAR(2),
    PesoLiquidoCarga FLOAT,
    FOREIGN KEY (IDAtracacao) REFERENCES atracacao_fato(IDAtracacao) ON DELETE CASCADE
);
