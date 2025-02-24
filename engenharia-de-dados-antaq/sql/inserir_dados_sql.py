import jaydebeapi
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace, lit
from pyspark.sql.types import IntegerType, DoubleType

"""
Script to insert data into SQL Server from Parquet files stored in the Data Lake.

This script performs:
1. Creation of a Spark session.
2. Reading and preprocessing of the Parquet files for "atracação" and "carga".
3. Standardization of column names and handling of inconsistent data.
4. Batch insertion of data into SQL Server for better performance.

Requirements:
- SQL Server must be preconfigured.
- Correct path to the Parquet files in the Data Lake.
- SQL Server JDBC driver properly set up.
"""

# 🔧 SQL Server Configuration
SERVER = "localhost"
DATABASE = "observatorio_industria"
USERNAME = "sa"
PASSWORD = "YourStrongPassword123"

# 🔧 Path to SQL Server JDBC driver
JDBC_DRIVER_PATH = "/mnt/c/Users/allys/OneDrive/Documentos/GitHub/engenharia-de-dados-antaq/sqljdbc_12.8/ptb/jars/mssql-jdbc-12.8.1.jre11.jar"

# 🔥 Create Spark session
spark = SparkSession.builder \
    .appName("Insert_SQL_Server") \
    .config("spark.driver.extraClassPath", JDBC_DRIVER_PATH) \
    .config("spark.executor.extraClassPath", JDBC_DRIVER_PATH) \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .getOrCreate()

# 📂 Data Lake Path
base_path = "/mnt/c/Users/allys/OneDrive/Documentos/GitHub/engenharia-de-dados-antaq/engenharia-de-dados-antaq/airflow/data/datalake"

# 📂 Read Parquet files
df_atracacao = spark.read.parquet(f"file://{base_path}/atracacao.parquet")
df_carga = spark.read.parquet(f"file://{base_path}/carga.parquet")

def standardize_column_names(df):
    """
    Standardizes column names to avoid compatibility issues.

    Parameters:
    df (DataFrame): PySpark DataFrame to be adjusted.

    Returns:
    DataFrame with standardized column names.
    """
    for column in df.columns:
        new_name = column.lower().replace(" ", "_").replace("ã", "a").replace("ç", "c").replace("é", "e")
        df = df.withColumnRenamed(column, new_name)
    return df

# Apply standardization
df_atracacao = standardize_column_names(df_atracacao)
df_carga = standardize_column_names(df_carga)

# 🔄 Data type adjustments and data cleaning
df_carga = df_carga.withColumn("teu", regexp_replace(col("teu"), "[^0-9.,]", ""))
df_carga = df_carga.withColumn("teu", regexp_replace(col("teu"), ",", ".").cast(DoubleType()))
df_carga = df_carga.withColumn("qtcarga", regexp_replace(col("qtcarga"), "[^0-9]", "").cast(IntegerType()))

# 🚀 Remove nonexistent columns to avoid schema errors
columns_to_exclude_atracacao = ["coordenadas"]
columns_to_exclude_carga = ["carga_geral_acondicionamento"]

for column in columns_to_exclude_atracacao:
    if column in df_atracacao.columns:
        df_atracacao = df_atracacao.drop(column)

for column in columns_to_exclude_carga:
    if column in df_carga.columns:
        df_carga = df_carga.drop(column)

# 🔄 Replace month names with numbers
month_mapping = {
    "jan": "1", "fev": "2", "mar": "3", "abr": "4", "mai": "5",
    "jun": "6", "jul": "7", "ago": "8", "set": "9", "out": "10",
    "nov": "11", "dez": "12"
}

for month, number in month_mapping.items():
    df_atracacao = df_atracacao.withColumn("mes", when(col("mes") == month, number).otherwise(col("mes")))

# 🔄 Replace invalid values with None
df_atracacao = df_atracacao.replace(["NaN", "NULL", "None"], None)
df_carga = df_carga.replace(["NaN", "NULL", "None"], None)

# 🔄 Convert columns to INT or FLOAT
df_atracacao = df_atracacao.withColumn("ano", col("ano").cast(IntegerType()))
df_atracacao = df_atracacao.withColumn("mes", col("mes").cast(IntegerType()))
df_atracacao = df_atracacao.withColumn("flagmcoperacaoatracacao", col("flagmcoperacaoatracacao").cast(IntegerType()))

df_carga = df_carga.withColumn("teu", col("teu").cast(DoubleType()))
df_carga = df_carga.withColumn("qtcarga", col("qtcarga").cast(IntegerType()))

# 🚀 Adjust for missing fields in schema
required_columns_atracacao = ["porto_atracacao", "complexo_portuario"]
for column in required_columns_atracacao:
    if column not in df_atracacao.columns:
        df_atracacao = df_atracacao.withColumn(column, lit(None).cast("string"))

required_columns_carga = ["tipo_operacao_carga"]
for column in required_columns_carga:
    if column not in df_carga.columns:
        df_carga = df_carga.withColumn(column, lit(None).cast("string"))

def insert_data_in_batches(df_spark, table, batch_size=10000):
    """
    Inserts data into SQL Server in batches to prevent memory overflow.

    Parameters:
    df_spark (DataFrame): PySpark DataFrame to be inserted.
    table (str): Name of the table in SQL Server.
    batch_size (int): Batch size for insertion.

    Returns:
    None
    """
    try:
        print(f"🚀 Starting data insertion into table {table}...")

        df_spark.selectExpr(*[f"`{col}` AS `{col}`" for col in df_spark.columns]) \
            .write \
            .format("jdbc") \
            .option("url", f"jdbc:sqlserver://{SERVER}:1433;databaseName={DATABASE};encrypt=false;trustServerCertificate=true") \
            .option("dbtable", table) \
            .option("user", USERNAME) \
            .option("password", PASSWORD) \
            .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
            .option("batchsize", batch_size) \
            .mode("append") \
            .save()

        print(f"✅ Data successfully inserted into table {table}")

    except Exception as e:
        print(f"⚠ Error inserting data into table {table}: {e}")

# 🔗 Connect to SQL Server and insert data
conn = None
try:
    conn = jaydebeapi.connect(
        "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        f"jdbc:sqlserver://{SERVER}:1433;databaseName={DATABASE};encrypt=false;trustServerCertificate=true",
        [USERNAME, PASSWORD],
        JDBC_DRIVER_PATH
    )
    print("✅ SQL Server connection established!")

    insert_data_in_batches(df_atracacao, "atracacao_fato")
    insert_data_in_batches(df_carga, "carga_fato")

except Exception as e:
    print(f"❌ Failed to connect to SQL Server: {e}")

finally:
    if conn:
        conn.close()
        print("✅ SQL Server connection closed.")
