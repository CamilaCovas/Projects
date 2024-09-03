FROM python:3.8-slim

# Instalar Apache Airflow y otras dependencias necesarias
RUN pip install apache-airflow

# Crear directorios necesarios
RUN mkdir -p /usr/local/airflow/dags

# Copiar el DAG y el script
COPY dags/countries_dag.py /usr/local/airflow/dags/
COPY scripts/ejercicio_3.py /usr/local/airflow/dags/

# Establecer variables de entorno necesarias
ENV AIRFLOW_HOME=/usr/local/airflow

# Inicializar la base de datos
RUN airflow db init

# Copiar el entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Usar el entrypoint para inicializar la base de datos y ejecutar Airflow
ENTRYPOINT ["/entrypoint.sh"]
