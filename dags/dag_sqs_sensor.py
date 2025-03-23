from airflow import DAG
from airflow.providers.amazon.aws.sensors.sqs import SqsSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

AWS_CONN_ID = "aws_local-stack"
SQS_QUEUE_URL = "https://localhost.localstack.cloud:4566/000000000000/sqs-dev-andre"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"
AWS_REGION = "us-east-1"

# Definir a função para processar a mensagem
def process_message(**kwargs):
    messages = kwargs['ti'].xcom_pull(task_ids='wait_for_sqs_message')
    if messages:
        for msg in messages:
            print(f"Mensagem recebida: {msg['Body']}")

# Definir a DAG
with DAG(
    dag_id="sqs_sensor_example",
    start_date=datetime(2024, 3, 22),
    schedule_interval=None,
    catchup=False,
) as dag:

    wait_for_sqs_message = SqsSensor(
        task_id="wait_for_sqs_message",
        sqs_queue=SQS_QUEUE_URL,
        aws_conn_id=AWS_CONN_ID,
        region_name=AWS_REGION,
        timeout=60,  # Espera até 60s
        max_messages=1,
        poke_interval=5
    )

    process_task = PythonOperator(
        task_id="process_message",
        python_callable=process_message,
        provide_context=True
    )

    wait_for_sqs_message >> process_task
