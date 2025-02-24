import os
import sys
import pandas as pd
import zipfile
import findspark
from pyspark.sql import SparkSession

"""
ANTAQ Data Processing Script.

This script:
1. Initializes PySpark and configures optimization parameters.
2. Defines paths for download directories and the Data Lake.
3. Processes downloaded ZIP files, extracts them, and converts the data into Parquet format.
4. Validates the generated Parquet files.

Requirements:
- ZIP files for "atracação" and "carga" must be downloaded in the designated directory.
"""

# Initialize findspark
findspark.init()

# Configure PySpark executables to use the correct Python version
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

# Initialize Spark with memory optimization settings
spark = (
    SparkSession.builder.appName("ANTAQ Processing")
    .config("spark.driver.memory", "4g")  # Increase memory for the driver
    .config("spark.executor.memory", "3g")  # Increase memory for executors
    .config("spark.sql.shuffle.partitions", "10")  # Reduce partitions for efficiency
    .config("spark.sql.files.maxPartitionBytes", "64MB")  # Control partition size
    .getOrCreate()
)

# Define corrected paths
base_dir = os.path.abspath(os.path.dirname(__file__))
download_path = os.path.abspath(os.path.join(base_dir, "..", "data", "downloads"))
data_lake_path = os.path.abspath(os.path.join(base_dir, "..", "data", "datalake"))

print(f"📂 Base Directory: {base_dir}")
print(f"📥 Download Path: {download_path} - Exists? {os.path.exists(download_path)}")
print(f"📤 Data Lake Path: {data_lake_path} - Exists? {os.path.exists(data_lake_path)}")

# Create the Data Lake folder if it doesn't exist
os.makedirs(data_lake_path, exist_ok=True)

def process_files():
    """
    Processes downloaded ZIP files by extracting and converting "atracação" and "carga" data into Parquet format.
    """
    if not os.path.exists(download_path):
        print("❌ Download path not found. Check directory structure.")
        return

    for file in os.listdir(download_path):
        if file.endswith(".zip"):
            file_path = os.path.join(download_path, file)

            # Extract ZIP files
            try:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(download_path)
                print(f"📂 File {file} successfully extracted.")
            except zipfile.BadZipFile:
                print(f"❌ Error: Corrupted ZIP file - {file}")
                continue

            # Identify the type of data
            if "Atracacao" in file:
                data_type = "atracacao"
            elif "Carga" in file:
                data_type = "carga"
            else:
                continue  # Skip irrelevant files

            # Process extracted TXT files
            for extracted in os.listdir(download_path):
                if extracted.endswith(".txt") and data_type in extracted.lower():
                    csv_path = os.path.join(download_path, extracted)

                    # Check if the CSV file is empty
                    if os.stat(csv_path).st_size == 0:
                        print(f"⚠️ File {csv_path} is empty. Skipping...")
                        continue

                    # Read data in chunks to avoid memory overflow
                    chunk_size = 100000
                    try:
                        df_iter = pd.read_csv(
                            csv_path, delimiter=";", encoding="utf-8", dtype=str, low_memory=False, chunksize=chunk_size
                        )
                    except Exception as e:
                        print(f"❌ Error reading {csv_path}: {e}")
                        continue

                    destination_parquet = os.path.join(data_lake_path, f"{data_type}.parquet")

                    # Process and save chunks in Parquet format
                    for i, chunk in enumerate(df_iter):
                        df_spark = spark.createDataFrame(chunk)
                        if i == 0:
                            df_spark.write.mode("overwrite").parquet(destination_parquet)
                        else:
                            df_spark.write.mode("append").parquet(destination_parquet)

                    print(f"✅ {data_type} processed and stored in Data Lake: {destination_parquet}")

# Execute processing
process_files()
print("🎯 All data has been successfully processed and stored in the Data Lake!")

def validate_parquet(file_path):
    """
    Validates the existence of generated Parquet files and displays a sample of their content.
    """
    if os.path.exists(file_path):
        df = spark.read.parquet(file_path)
        total_records = df.count()
        print(f"✅ File {file_path} contains {total_records} records.")
        df.show(5)
    else:
        print(f"❌ File {file_path} not found!")

# Validate processed Parquet files
validate_parquet(os.path.join(data_lake_path, "atracacao.parquet"))
validate_parquet(os.path.join(data_lake_path, "carga.parquet"))
