FROM python:3.8-slim

# Instalar dependencias necesarias
RUN pip install apache-airflow pandas requests psycopg2

# Crear directorios necesarios
RUN mkdir -p /usr/local/airflow/dags

# Copiar el DAG y el script
COPY countries_dag.py /usr/local/airflow/dags/
COPY ejercicio_3.py /usr/local/airflow/dags/

# Establecer variables de entorno necesarias
ENV AIRFLOW_HOME=/usr/local/airflow

# Inicializar la base de datos
RUN airflow db init

# Copiar el entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Usar el entrypoint para inicializar la base de datos y ejecutar Airflow
ENTRYPOINT ["/entrypoint.sh"]
