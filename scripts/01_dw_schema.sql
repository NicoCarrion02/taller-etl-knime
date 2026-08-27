-- ==========================================
-- DDL para el Data Warehouse f1_dw
-- Modelo Estrella: 5 Dimensiones, 1 Fact Table
-- ==========================================

-- Limpieza previa (Idempotencia)
DROP TABLE IF EXISTS fact_results CASCADE;
DROP TABLE IF EXISTS dim_status CASCADE;
DROP TABLE IF EXISTS dim_races_time CASCADE;
DROP TABLE IF EXISTS dim_circuits CASCADE;
DROP TABLE IF EXISTS dim_constructors CASCADE;
DROP TABLE IF EXISTS dim_drivers CASCADE;

-- 1. Dimensión Pilotos
CREATE TABLE dim_drivers (
    driver_id INT PRIMARY KEY,
    driver_ref VARCHAR(255),
    full_name VARCHAR(255),
    nationality VARCHAR(100),
    dob DATE
);

-- 2. Dimensión Constructores (Escuderías)
CREATE TABLE dim_constructors (
    constructor_id INT PRIMARY KEY,
    constructor_ref VARCHAR(255),
    name VARCHAR(255),
    nationality VARCHAR(100)
);

-- 3. Dimensión Circuitos
CREATE TABLE dim_circuits (
    circuit_id INT PRIMARY KEY,
    circuit_ref VARCHAR(255),
    name VARCHAR(255),
    location VARCHAR(255),
    country VARCHAR(100)
);

-- 4. Dimensión Tiempo / Carreras
CREATE TABLE dim_races_time (
    race_id INT PRIMARY KEY,
    year INT,
    round INT,
    name VARCHAR(255),
    date DATE
);

-- 5. Dimensión Estatus
CREATE TABLE dim_status (
    status_id INT PRIMARY KEY,
    status VARCHAR(255)
);

-- 6. Tabla de Hechos: Resultados
CREATE TABLE fact_results (
    result_id INT PRIMARY KEY,
    race_id INT,
    driver_id INT,
    constructor_id INT,
    circuit_id INT,
    status_id INT,
    grid INT,
    position_order INT,
    points FLOAT,
    laps INT,
    milliseconds BIGINT,
    
    -- Relaciones (Foreign Keys)
    FOREIGN KEY (race_id) REFERENCES dim_races_time(race_id),
    FOREIGN KEY (driver_id) REFERENCES dim_drivers(driver_id),
    FOREIGN KEY (constructor_id) REFERENCES dim_constructors(constructor_id),
    FOREIGN KEY (circuit_id) REFERENCES dim_circuits(circuit_id),
    FOREIGN KEY (status_id) REFERENCES dim_status(status_id)
);