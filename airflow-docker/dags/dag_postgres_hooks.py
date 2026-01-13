
import csv
import logging
from datetime import datetime, timedelta
from tempfile import NamedTemporaryFile

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}


def postgres_to_s3(**context):
    data_interval_start = context["prev_data_interval_start_success"]
    data_interval_end   = context["data_interval_start"]
    start_key = data_interval_start.strftime("%Y-%m-%d")
    logging.info("Start Key: %s", {start_key})
    end_key   = data_interval_end.strftime("%Y-%m-%d")
    logging.info("End Key: %s", {end_key})

    # step 1: query data from postgresql db and save into text file
    hook = PostgresHook(postgres_conn_id="postgres_localhost")
    conn = hook.get_conn()
    cursor = conn.cursor()
    # Fetch order date for previous day and current day
    cursor.execute("select * from orders where date >= %s and date <= %s",
                   (start_key, end_key))
    #cursor.execute("select * from orders where date >= '2018-04-30' and date < '2025-05-01'")
    with NamedTemporaryFile(mode='w', suffix=f"{start_key}") as f:
    # with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)
        f.flush()
        cursor.close()
        conn.close()
        logging.info("Saved orders data in text file: %s", f"dags/get_orders_{start_key}.txt")
    # step 2: upload text file into S3
        s3_hook = S3Hook(aws_conn_id="minio_conn")
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/{start_key}.txt",
            bucket_name="airflow",
            replace=True
        )
        logging.info("Orders file %s has been pushed to S3!", f.name)


with DAG(
    dag_id="dag_postgres_hooks_v01",
    default_args=default_args,
    start_date=datetime(2022, 4, 30),
    schedule='@daily'
) as dag:
    task1 = PythonOperator(
        task_id="postgres_to_s3",
        python_callable=postgres_to_s3
    )
    task1
