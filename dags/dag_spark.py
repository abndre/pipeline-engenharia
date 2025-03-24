from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Argumentos padrão da DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 21),
    "retries": 0,
}

# Criando a DAG
dag = DAG(
    "spark_pi_example",
    default_args=default_args,
    description="Executa o exemplo Spark Pi",
    schedule_interval=None,  # Executa manualmente
    catchup=False,
)

# Comando para rodar o Spark
spark_command = """
spark-submit --master local[*] \
    /opt/airflow/spark_scripts/pi.py 10
"""

# Task que executa o Spark
run_spark_pi = BashOperator(
    task_id="run_spark_pi",
    bash_command=spark_command,
    dag=dag,
)

# Definir a ordem das tarefas
run_spark_pi
