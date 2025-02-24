from pyspark.sql import SparkSession

"""
ANTAQ Data Exploration Script.

This script performs:
1. Creation of a Spark session.
2. Reading of Parquet files for "atracação" and "carga" stored in the Data Lake.
3. Display of the structure of the loaded DataFrames.
4. Presentation of data samples for validation.
5. Counting the total number of records in each dataset.

Requirements:
- The files `atracacao.parquet` and `carga.parquet` must be stored in the Data Lake.
"""

# Create a Spark session
spark = SparkSession.builder \
    .appName("ANTAQ Data Exploration") \
    .getOrCreate()

# Define the paths of Parquet files in the Data Lake
path_atracacao = "/mnt/c/Users/allys/OneDrive/Documentos/GitHub/engenharia-de-dados-antaq/engenharia-de-dados-antaq/airflow/data/datalake/atracacao.parquet"
path_carga = "/mnt/c/Users/allys/OneDrive/Documentos/GitHub/engenharia-de-dados-antaq/engenharia-de-dados-antaq/airflow/data/datalake/carga.parquet"

# Read Parquet files using PySpark
df_atracacao = spark.read.parquet(path_atracacao)
df_carga = spark.read.parquet(path_carga)

def explore_dataframe(df, name):
    """
    Displays the structure and a sample of data from a DataFrame.

    Parameters:
    df (DataFrame): PySpark DataFrame to be analyzed.
    name (str): Name of the DataFrame for identification in the output.
    """
    print(f"\n📌 Structure of DataFrame {name}:")
    df.printSchema()

    print(f"\n📌 Sample data from {name}:")
    df.show(5)

    total_records = df.count()
    print(f"✅ File {name} contains {total_records} records.")

# Explore the DataFrames
explore_dataframe(df_atracacao, "Atracacao")
explore_dataframe(df_carga, "Carga")

print("\n🎯 Analysis completed!")
