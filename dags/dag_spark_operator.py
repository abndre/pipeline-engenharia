from airflow import DAG
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from datetime import datetime

# Argumentos padrão da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 21),
    "retries": 1,
}

# Criando a DAG
dag = DAG(
    "spark_pi_example",
    default_args=default_args,
    description="Executa o exemplo Spark Pi",
    schedule_interval=None,  # Executa manualmente
    catchup=False,
)

# Comando para rodar o Spark com o SparkSubmitOperator
run_spark_pi = SparkSubmitOperator(
    task_id="run_spark_pi",
    conn_id="spark_default",  # O Airflow usa esse ID de conexão para a configuração do Spark
    application="/opt/spark/examples/src/main/python/pi.py",  # Caminho do exemplo do Spark
    total_executor_cores=4,  # Número de núcleos para os executores
    executor_memory="1G",  # Memória para cada executor
    driver_memory="1G",  # Memória para o driver
    name="spark_pi_example",  # Nome da aplicação no Spark
    verbose=True,  # Mostrar logs detalhados
    dag=dag,
)

# Ordem das tarefas
run_spark_pi
