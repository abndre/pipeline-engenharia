from airflow import DAG
#from airflow.providers.amazon.aws.sensors.sqs import SQSSensor
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import boto3

# Configurações da conexão AWS para LocalStack
AWS_CONN_ID = "aws_local-stack"
SQS_QUEUE_URL = "https://localhost.localstack.cloud:4566/000000000000/sqs-dev-andre"
AWS_ACCESS_KEY = "test"
AWS_SECRET_KEY = "test"
AWS_REGION = "us-east-1"

def process_message(**kwargs):
    """Função para ler mensagens da fila SQS"""
    sqs_client = boto3.client(
        "sqs",
        region_name=AWS_REGION,
        endpoint_url="http://localstack:4566",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    
    response = sqs_client.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10
    )
    
    messages = response.get("Messages", [])
    
    for message in messages:
        body = json.loads(message.get("Body", "{}"))
        print(f"Mensagem recebida: {body}")
        
        # Excluindo a mensagem após o processamento
        sqs_client.delete_message(
            QueueUrl=SQS_QUEUE_URL,
            ReceiptHandle=message["ReceiptHandle"]
        )
        print("Mensagem deletada da fila.")

# Definição da DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 21),
    'retries': 0
}

dag = DAG(
    dag_id='sqs_localstack_dag',
    default_args=default_args,
    schedule_interval=None,  # Executa manualmente ou via trigger
    catchup=False
)

# Tarefa que lê a mensagem da fila SQS
read_sqs_task = PythonOperator(
    task_id='read_sqs_message_task',
    python_callable=process_message,
    dag=dag
)

read_sqs_task
