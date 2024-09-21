-- Crear la tabla "combined_data" en Amazon Redshift si no existe
CREATE TABLE IF NOT EXISTS public.combined_data (
    country_name VARCHAR(100),               -- Nombre del país
    capital VARCHAR(100),                    -- Capital del país
    population BIGINT,                       -- Población del país
    sales_amount DECIMAL(10, 2),             -- Cantidad de ventas simuladas
    extraction_date TIMESTAMP DEFAULT SYSDATE,  -- Fecha y hora de extracción de los datos
    data_date TIMESTAMP,                     -- Fecha en la que se generaron los datos
    alert_flag BOOLEAN DEFAULT FALSE         -- Bandera que indica si se ha enviado una alerta
);

-- Insertar datos en la tabla "combined_data"
INSERT INTO public.combined_data (country_name, capital, population, sales_amount, data_date)
VALUES 
('Argentina', 'Buenos Aires', 45195777, 100000.50, '2024-09-21 00:00:00'),
('Brazil', 'Brasilia', 212559417, 150000.75, '2024-09-21 00:00:00'),
('Chile', 'Santiago', 19116201, 120000.30, '2024-09-21 00:00:00'),
('Mexico', 'Ciudad de Mexico', 126190788, 200000.95, '2024-09-21 00:00:00');
