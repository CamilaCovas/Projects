import requests
import pandas as pd
from sqlalchemy import create_engine

def extract_data():
    url = 'https://restcountries.com/v3.1/all'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")

def transform_data(data):
    countries = []
    for country in data:
        name = country.get('name', {}).get('common', '')
        capital = country.get('capital', [''])[0]
        region = country.get('region', '')
        subregion = country.get('subregion', '')
        population = country.get('population', 0)
        area = country.get('area', 0.0)
        
        if not isinstance(population, int):
            population = 0
        
        if not isinstance(area, (int, float)):
            area = 0.0

        country_info = {
            'name': name,
            'capital': capital,
            'region': region,
            'subregion': subregion,
            'population': population,
            'area': area
        }
        countries.append(country_info)

    df = pd.DataFrame(countries)
    return df

def load_data(df):
    engine = create_engine('postgresql+psycopg2://<username>:<password>@<redshift-cluster-endpoint>:5439/<database>')
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS countries (
        name VARCHAR(255),
        capital VARCHAR(255),
        region VARCHAR(255),
        subregion VARCHAR(255),
        population BIGINT,
        area FLOAT,
        PRIMARY KEY (name, capital)
    );
    """
    with engine.connect() as conn:
        conn.execute(create_table_query)
    
    df.to_sql('countries', engine, if_exists='replace', index=False)

def main():
    data = extract_data()
    df = transform_data(data)
    load_data(df)

if __name__ == "__main__":
    main()

