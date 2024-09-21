#!/bin/bash

# Salir inmediatamente si cualquier comando falla
set -e

# Imprimir todos los comandos para debug
set -x

# Inicializar la base de datos de Airflow
airflow db init

# Crear el usuario administrador para la interfaz de Airflow (si es necesario)
airflow users create \
    --username admin \
    --password admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com

# Ejecutar el scheduler en segundo plano
airflow scheduler &

# Ejecutar el servidor web de Airflow en el puerto 8080
exec airflow webserver --port 8080
