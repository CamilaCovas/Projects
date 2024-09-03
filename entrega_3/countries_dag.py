from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2

# Definir los argumentos del DAG
default_args = {
    'owner': 'usuario_airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Crear el objeto DAG
dag = DAG(
    'countries_dag',
    default_args=default_args,
    description='Un DAG simple para cargar datos en Redshift',
    schedule_interval='@daily',  # Programar para que se ejecute diariamente
    catchup=False  # Evitar la ejecución retroactiva de tareas
)

def cargar_datos_redshift():
    # Configuración de la conexión a Redshift
    dbname = 'data-engineer-database'
    user = 'covascamilaf_coderhouse'
    password = 'V3F6Up6vV6'
    host = 'http://data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com/'
    port = '5439'  

    try:
        # Conexión a Redshift
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        cur = conn.cursor()

        # Datos de muestra para insertar en la tabla
        datos_muestra = [
            (1, 'Argentina', 'Buenos Aires'),
            (2, 'Brasil', 'Sao Paulo'),
            (3, 'Chile', 'Santiago'),
        ]

        # Insertar datos de muestra en la tabla countries
        for dato in datos_muestra:
            cur.execute("INSERT INTO countries (id, country_name, capital) VALUES (%s, %s, %s)", dato)

        # Confirmar los cambios y cerrar la conexión
        conn.commit()
        print("Datos de muestra insertados correctamente en la tabla countries.")

    except psycopg2.Error as e:
        print(f"Error al conectar a Redshift o al insertar datos: {e}")

    finally:
        # Cerrar la conexión al finalizar
        if conn is not None:
            conn.close()

# Definir una tarea utilizando PythonOperator
cargar_datos_task = PythonOperator(
    task_id='cargar_datos_redshift_task',
    python_callable=cargar_datos_redshift,
    dag=dag
)

# Establecer la secuencia de tareas
cargar_datos_task

