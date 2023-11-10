"""
Simple DAG to process web logs
"""

import tarfile
from datetime import timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

BASE_PATH = Path(__file__).parent
STAGING_DIR = BASE_PATH / "capstone" 

default_args = {
    "owner": "philsv",
    "start_date": days_ago(0),
    "email": "philsv@example.com",
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    dag_id="process_web_logs",
    default_args=default_args,
    description="A simple DAG to process web logs",
    schedule_interval=timedelta(days=1),
)


def extract_data_func() -> None:
    """
    Extract data from the web logs
    """
    input_file_path = STAGING_DIR / "accesslog.txt"
    output_file_path = STAGING_DIR / "extracted_data.txt"

    with open(input_file_path, "r") as input_file, open(
        output_file_path, "w"
    ) as output_file:
        for line in input_file:
            # Extract IP address
            first_column = line.split()[0]
            output_file.write(first_column + "\n")


extract_data = PythonOperator(
    task_id="extract_data",
    python_callable=extract_data_func,
    dag=dag,
)


def transform_data_func() -> None:
    """
    Transform data from the web logs
    """
    input_file_path = STAGING_DIR / "extracted_data.txt"
    output_file_path = STAGING_DIR / "transformed_data.txt"

    with open(input_file_path, "r") as input_file, open(
        output_file_path, "w"
    ) as output_file:
        for line in input_file:
            # Exclude lines containing "198.46.149.143"
            if "198.46.149.143" not in line:
                output_file.write(line)


transform_data = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data_func,
    dag=dag,
)


def load_data_func() -> None:
    """
    Load data from the web logs into a tar archive
    """
    input_file_path = STAGING_DIR / "transformed_data.txt"
    output_archive_path = STAGING_DIR / "weblog.tar"

    with tarfile.open(output_archive_path, "w") as archive:
        archive.add(input_file_path, arcname="transformed_data.txt")


load_data = PythonOperator(
    task_id="load_data",
    python_callable=load_data_func,
    dag=dag,
)


# Task Pipeline
extract_data >> transform_data >> load_data
