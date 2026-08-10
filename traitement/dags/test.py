import uuid
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import  MongoClient


default_args = {
    'owner': 'atou',
    'start_date': datetime(2023, 9, 3, 10, 00)
}

def get_data():

    data = []

    url = "mongodb://172.18.0.3:27017"

    my_database = "test_airflow"
    my_collection = "airflow"

    client = MongoClient(url)
    print(client)
    db = client[my_database]
    print(db)

    collection = db[my_collection]
    print(collection)

    results = collection.find()


    for result in results:
        print(result)


    return data






def hi():

    return  'hi'



def get():


    return  'get you all'


with DAG('test',
         default_args=default_args,
         schedule_interval=timedelta(minutes=1),#'@daily',
         catchup=False) as dag:

    task_1 = PythonOperator(
        task_id='task1',
        python_callable=get_data
    )

    task_2 = PythonOperator(
        task_id='task2',
        python_callable=hi,
    )

    task_3 = PythonOperator(
        task_id='task3',
        python_callable=get,
        provide_context=True,
        dag=dag

    )



    task_1 >> task_2 >> task_3