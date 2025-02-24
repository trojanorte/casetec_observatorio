import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

"""
ETL Pipeline for ANTAQ Data using Apache Airflow.

This DAG executes the following steps every 15 days:
1. Checks if data exists in the Data Lake.
2. Downloads new data if needed.
3. Processes the data (ETL).
4. Sends an email notification upon completion.
"""

# Default DAG arguments
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 2, 20),
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Define DAG
dag = DAG(
    "antaq_etl_pipeline",
    default_args=default_args,
    description="ETL Pipeline for ANTAQ Data",
    schedule_interval=timedelta(days=15),  # Runs every 15 days
    catchup=False,
)

def check_data_availability():
    """
    Checks if there are files in the Data Lake before starting the ETL pipeline.
    Raises an error if no files are found to prevent further execution.
    """
    data_path = "/opt/airflow/data/datalake/"
    files = os.listdir(data_path)
    if not files:
        raise ValueError("⚠ No files found in the Data Lake!")

def download_data():
    """
    Executes the script responsible for downloading ANTAQ data.
    """
    os.system("python /opt/airflow/dags/scripts/download_dados.py")

def process_data():
    """
    Executes the ETL pipeline to transform and load the processed data into the database.
    """
    os.system("python /opt/airflow/dags/scripts/etl_pipeline.py")

# Task 1: Check Data Availability
check_data_task = PythonOperator(
    task_id="check_data_availability",
    python_callable=check_data_availability,
    dag=dag,
)

# Task 2: Download Data
download_data_task = PythonOperator(
    task_id="download_data",
    python_callable=download_data,
    dag=dag,
)

# Task 3: Process Data (ETL)
process_data_task = PythonOperator(
    task_id="process_data",
    python_callable=process_data,
    dag=dag,
)

# Task 4: Send Success Email
email_success_task = EmailOperator(
    task_id="email_success",
    to="allysonaires@email.com",
    subject="ETL Successfully Completed 🚀",
    html_content="The ETL process for ANTAQ data has been successfully completed! ✅",
    dag=dag,
)

# Define Execution Order
check_data_task >> download_data_task >> process_data_task >> email_success_task
