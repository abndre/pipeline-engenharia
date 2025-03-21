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
import os
# Configurações do MinIO/S3
AWS_ACCESS_KEY_ID = "admin"
AWS_SECRET_ACCESS_KEY = "password"
S3_ENDPOINT_URL = "http://minio:9000"
BUCKET_NAME = "warehouse"
OBJECT_NAME = "data/dados.csv"

def create_and_upload_dataframe():
    # Criar DataFrame
    data = {"Nome": ["Alice", "Bob", "Charlie"], "Idade": [25, 30, 35]}
    df = pd.DataFrame(data)

    # Salvar como CSV em um arquivo temporário
    temp_file = "/tmp/dados.csv"
    df.to_csv(temp_file, index=False)

    # Upload para o S3
    s3_hook = S3Hook(aws_conn_id="aws_default")
    s3_hook.load_file(filename=temp_file, bucket_name=BUCKET_NAME, key=OBJECT_NAME, replace=True)

    # Remover arquivo temporário
    os.remove(temp_file)
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

    upload_task
run_this >> list_task >> list_files >> upload_task