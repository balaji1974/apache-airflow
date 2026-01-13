from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'balaji',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id='dag_sensor_s3_v1',
    start_date=datetime(2025,12, 31),
    schedule='@daily',
    default_args=default_args
) as dag:
    task1 = S3KeySensor(
        task_id='dag_sensor_s3',
        bucket_name='airflow',
        bucket_key='data.csv',
        aws_conn_id='minio_conn',
        mode='poke',
        poke_interval=5,
        timeout=30
    )