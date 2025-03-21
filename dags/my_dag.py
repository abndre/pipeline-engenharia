import time
from pprint import pprint
import pendulum
import boto3
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
import pandas as pd
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os, io
# Configurações do MinIO/S3
AWS_ACCESS_KEY_ID = "admin"
AWS_SECRET_ACCESS_KEY = "password"
S3_ENDPOINT_URL = "http://minio:9000"
BUCKET_NAME = "warehouse"
OBJECT_NAME = "data/dados.csv"

def read_csv_from_s3():
    # Criar instância do S3Hook
    s3_hook = S3Hook(aws_conn_id="aws_default")
    
    # Obter o arquivo do S3 como um objeto em memória
    file_obj = s3_hook.get_key(key=OBJECT_NAME, bucket_name=BUCKET_NAME)

    # Converter o conteúdo para um arquivo em memória
    file_stream = io.StringIO(file_obj.get()['Body'].read().decode('utf-8'))

    # Ler o CSV com Pandas
    df = pd.read_csv(file_stream)
    print(df)

def create_and_upload_dataframe():
    # Criar DataFrame
    data = {"Nome": ["Alice", "Bob", "Charlie"], "Idade": [25, 30, 35]}
    df = pd.DataFrame(data)

    # Salvar como CSV em um buffer de memória
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)  # Reposicionar o ponteiro no início do buffer

    # Upload para o S3 usando load_bytes
    s3_hook = S3Hook(aws_conn_id="aws_default")
    s3_hook.load_bytes(bytes_data=csv_buffer.getvalue().encode('utf-8'), bucket_name=BUCKET_NAME, key=OBJECT_NAME, replace=True)

    print(f"Arquivo {OBJECT_NAME} enviado para {BUCKET_NAME}")


def list_s3_bucket():
    """Lista os arquivos dentro do bucket S3/MinIO."""
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=S3_ENDPOINT_URL
    )
    
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in response:
        files = [obj["Key"] for obj in response["Contents"]]
        print("Arquivos no bucket:", files)
    else:
        print("O bucket está vazio ou não existe.")

with DAG(
    dag_id='my_dag',
    schedule=None,
    start_date=pendulum.datetime(2022, 5, 11, 15,45, tz="America/Sao_Paulo"),
    catchup=False,
    tags=['example'],
) as dag:

    # [START howto_operator_python]
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        #pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = print_context()

    list_task = PythonOperator(
    task_id="list_s3_files",
    python_callable=list_s3_bucket,
    dag=dag,
    )

    list_files = S3ListOperator(
        task_id="list_files",
        bucket=BUCKET_NAME,
        prefix="",
        aws_conn_id="aws_default"
    )
    upload_task = PythonOperator(
            task_id="create_and_upload_dataframe",
            python_callable=create_and_upload_dataframe
        )


    read_task = PythonOperator(
        task_id="read_csv_from_s3",
        python_callable=read_csv_from_s3
    )

    
run_this >> list_task >> list_files >> upload_task >> read_task