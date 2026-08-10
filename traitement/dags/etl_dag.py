from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymongo

def extract():
    print("Extracting data...")
    return {"data": [1, 2, 3]}

def transform(**kwargs):
    data = kwargs['ti'].xcom_pull(task_ids='extract_task')
    transformed = [x * 2 for x in data["data"]]
    print(f"Transformed data: {transformed}")
    return transformed

def load(**kwargs):
    transformed_data = kwargs['ti'].xcom_pull(task_ids='transform_task')
    print(f"Loading data: {transformed_data}")

default_args = {
    'start_date': datetime(2025, 1, 1),

}

with DAG(
    'etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
) as dag:
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract,
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        provide_context=True,
    )

    extract_task >> transform_task >> load_task

