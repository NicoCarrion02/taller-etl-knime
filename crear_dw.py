import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DW_DB = "f1_dw"
SQL_FILE = "./scripts/01_dw_schema.sql"

print(f"[INFO] Iniciando configuración del Data Warehouse: {DW_DB}...")

try:
    pg_default_engine = create_engine(f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/postgres")
    
    with pg_default_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        db_exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DW_DB}'")).scalar()
        if not db_exists:
            conn.execute(text(f"CREATE DATABASE {DW_DB}"))
            print(f"[INFO] Base de datos '{DW_DB}' creada exitosamente.")
        else:
            print(f"[INFO] La base de datos '{DW_DB}' ya existe. Procediendo a actualizar esquemas.")

    pg_dw_engine = create_engine(f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{DW_DB}")
    
    with open(SQL_FILE, "r", encoding="utf-8") as file:
        sql_script = file.read()

    with pg_dw_engine.connect() as conn:
        conn.execute(text(sql_script))
        conn.commit()
        print("[INFO] Modelo estrella (tablas y relaciones) construido correctamente en el Data Warehouse.")

except Exception as e:
    print(f"[ERROR] Ocurrió un fallo al construir el DW: {e}")