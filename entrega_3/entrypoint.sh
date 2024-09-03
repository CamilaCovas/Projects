#!/bin/sh

# Inicializar la base de datos
airflow db init

# Iniciar el scheduler en segundo plano
airflow scheduler &

# Iniciar el webserver
exec airflow webserver
