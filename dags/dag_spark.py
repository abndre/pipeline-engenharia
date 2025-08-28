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
    schedule=None,  # Executa manualmente
    catchup=False,
)

# Comando para rodar o Spark
spark_command_pi = """
spark-submit --master local[*] \
    /opt/airflow/spark_scripts/pi.py
"""

# Comando para rodar o Spark
spark_command = """
spark-submit --master local[*] \
    /opt/airflow/spark_scripts/demo_iceberg_spark.py
"""

# Task que executa o Spark
run_spark_pi = BashOperator(
    task_id="run_spark_pi",
    bash_command=spark_command_pi,
    dag=dag,
)


# Task que executa o Spark
run_spark_iceberg = BashOperator(
    task_id="run_spark",
    bash_command=spark_command,
    dag=dag,
)

# Definir a ordem das tarefas
run_spark_pi >> run_spark_iceberg
