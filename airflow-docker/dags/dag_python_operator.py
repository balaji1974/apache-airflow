from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator


default_args = {
    'owner': 'balaji',
    'retry': 5,
    'retry_delay': timedelta(minutes=5)
}

def greet(name, age):
    print(f"Name is {name} and age is {age} ")

def get_sklearn():
    import sklearn
    print(f"sklearn with version: {sklearn.__version__} ")


def get_matplotlib():
    import matplotlib
    print(f"matplotlib with version: {matplotlib.__version__}")

def set_name():
    return "Balaji"

def get_name(ti):
    name = ti.xcom_pull(task_ids='set_name')
    print(f"Hello my name is {name}")

def set_multiple_values(ti):
    ti.xcom_push('first_name', "Balaji")
    ti.xcom_push('last_name', "Thiagarajan") 

def get_multiple_values(ti):
    first_name = ti.xcom_pull(task_ids='set_multiple_values', key='first_name')
    last_name = ti.xcom_pull(task_ids='set_multiple_values', key='last_name')
    print(f"Full name is {first_name} {last_name}") 

with DAG(
    default_args=default_args,
    dag_id="dag_python_operator_v8",
    start_date=datetime(2026, 1, 5),
    schedule='@daily'
) as dag:
    
    # Calling simple function and passing parameters to it using op_kwargs
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'name': 'Balaji', 'age': 30} 
    )
    
    # Calling python function which uses sklearn package
    task2 = PythonOperator(
        task_id='get_sklearn',
        python_callable=get_sklearn
    )
    
    # Calling python function which uses matplotlib package
    task3 = PythonOperator(
        task_id='get_matplotlib',
        python_callable=get_matplotlib
    )
    
    # Calling python function which returns a value
    # This value can be seen under Browse -> XComs
    task4 = PythonOperator(
        task_id='set_name',
        python_callable=set_name
    )

    # Reading the value from XComs (from another task)
    task5 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    # Calling python function which returns multiple value
    # This value can be seen under Browse -> XComs
    task6 = PythonOperator(
        task_id='set_multiple_values',
        python_callable=set_multiple_values
    )

    # Reading multiple values using XComs
    task7 = PythonOperator(
        task_id='get_multiple_values',
        python_callable=get_multiple_values
    )   
    
    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7