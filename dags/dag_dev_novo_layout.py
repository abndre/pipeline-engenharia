"""
Example DAG demonstrating the usage of ``@task.branch`` TaskFlow API decorator with depends_on_past=True,
where tasks may be run or skipped on alternating runs.
"""

from __future__ import annotations

import pendulum

from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.sdk import DAG, task


@task.branch()
def should_run(**kwargs) -> str:
    """
    Determine which empty_task should be run based on if the logical date minute is even or odd.

    :param dict kwargs: Context
    :return: Id of the task to run
    """
    print(f"------------- exec dttm = {kwargs['logical_date']} and minute = {kwargs['logical_date'].minute}")
    if kwargs["logical_date"].minute % 2 == 0:
        return "empty_task_1"
    return "empty_task_2"


with DAG(
    dag_id="example_branch_dop_operator_v3",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    default_args={"depends_on_past": True},
    tags=["example"],
) as dag:
    cond = should_run()

    empty_task_1 = EmptyOperator(task_id="empty_task_1")
    empty_task_2 = EmptyOperator(task_id="empty_task_2")
    cond >> [empty_task_1, empty_task_2]