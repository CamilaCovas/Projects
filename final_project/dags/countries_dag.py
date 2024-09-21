from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import ejercicio_3  # Asumiendo que el script de extracción está guardado como 'ejercicio_3.py'

default_args = {
    'owner': 'usuario_airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'countries_dag',
    default_args=default_args,
    description='Un DAG simple para cargar datos en Redshift',
    schedule_interval='@daily',
    catchup=False
)

# Definir las tareas
def ejecutar_pipeline():
    ejercicio_3.main()  # Asumiendo que la lógica completa está en la función `main` de `ejercicio_3.py`

pipeline_task = PythonOperator(
    task_id='ejecutar_pipeline',
    python_callable=ejecutar_pipeline,
    dag=dag
)

pipeline_task
