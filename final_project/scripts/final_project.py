import requests
import psycopg2
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Configuración de conexión a Redshift
dbname = 'data-engineer-database'
user = 'covascamilaf_coderhouse'
password = 'V3F6Up6vV6'
host = 'data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com'
port = '5439'

# Función para enviar alerta por correo
def enviar_alerta(correo_destino, asunto, mensaje):
    remitente = 'finalproject@example.com'
    password = 'final_project'
    
    msg = MIMEText(mensaje)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = correo_destino
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, correo_destino, msg.as_string())

# Extracción de datos desde la API pública
response = requests.get('https://restcountries.com/v3.1/all')
countries_data = response.json()

# Transformación de los datos con Pandas
df_countries = pd.DataFrame([{
    'country_name': country['name']['common'],
    'capital': country.get('capital', [''])[0],
    'population': country['population'],
    'area': country.get('area', 0)
} for country in countries_data])

# Simulación de una segunda fuente de datos: datos de ventas desde una base de datos (ejemplo local)
sales_data = [
    {'id': 1, 'fecha': '2024-09-01', 'producto': 'Producto A', 'cantidad': 10, 'monto': 150.50},
    {'id': 2, 'fecha': '2024-09-01', 'producto': 'Producto B', 'cantidad': 5, 'monto': 75.25},
]

df_sales = pd.DataFrame(sales_data)

# Combinación de los datos
df_combined = pd.concat([df_countries, df_sales], axis=1)

# Cargar los datos combinados a Redshift
try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    # Crear la tabla en Redshift
    cur.execute("""
        CREATE TABLE IF NOT EXISTS combined_data (
            country_name VARCHAR(255),
            capital VARCHAR(255),
            population BIGINT,
            area FLOAT,
            id INT,
            fecha DATE,
            producto VARCHAR(255),
            cantidad INT,
            monto FLOAT
        )
    """)

    # Insertar los datos transformados en la tabla
    for _, row in df_combined.iterrows():
        cur.execute("""
            INSERT INTO combined_data (country_name, capital, population, area, id, fecha, producto, cantidad, monto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, tuple(row))
    
    conn.commit()
    print("Datos insertados correctamente en Redshift")

except psycopg2.Error as e:
    print(f"Error al conectar o insertar en Redshift: {e}")

finally:
    if conn:
        conn.close()

# Enviar alertas si la población supera los 1,000,000,000
for _, row in df_countries.iterrows():
    if row['population'] > 1000000000:
        enviar_alerta('alerta@example.com', 'Alerta de población', f"La población de {row['country_name']} ha superado el umbral de 1,000,000,000 habitantes.")
