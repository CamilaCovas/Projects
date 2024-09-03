import psycopg2
from datetime import date

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
        (1, date(2024, 9, 1), 'Producto A', 10, 150.50),
        (2, date(2024, 9, 1), 'Producto B', 5, 75.25),
        (3, date(2024, 9, 2), 'Producto A', 8, 120.80),
    ]

    # Insertar datos de muestra en la tabla ventas
    for dato in datos_muestra:
        cur.execute("INSERT INTO ventas (id, fecha, producto, cantidad, monto) VALUES (%s, %s, %s, %s, %s)", dato)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    print("Datos de muestra insertados correctamente en la tabla ventas.")

except psycopg2.Error as e:
    print(f"Error al conectar a Redshift: {e}")

finally:
    # Cerrar la conexión al finalizar
    if conn is not None:
        conn.close()
