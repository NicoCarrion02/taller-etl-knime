import pandas as pd
import os
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

base_path = "./datasets/kaggle_f1/"
archivos = {
    "results": os.path.join(base_path, "results.csv"),
    "races": os.path.join(base_path, "races.csv"),
    "constructors": os.path.join(base_path, "constructors.csv"),
    "status": os.path.join(base_path, "status.csv"),
    "drivers": os.path.join(base_path, "drivers.csv")
    # circuits.csv no se carga, se leerá como archivo plano directamente en Knime
}

print("Iniciando preparación y carga de bases de datos en los contenedores Docker...")

# ==========================================
# 1. PostgreSQL (Creación y Carga)
# ==========================================
try:
    print("\n[1/3] Configurando PostgreSQL...")
    pg_default_engine = create_engine(f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/postgres")
    
    with pg_default_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        db_exists = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{os.getenv('PG_DB')}'")).scalar()
        if not db_exists:
            conn.execute(text(f"CREATE DATABASE {os.getenv('PG_DB')}"))
            print(f"[*] Base de datos '{os.getenv('PG_DB')}' creada en PostgreSQL.")
        else:
            print(f"[*] La base de datos '{os.getenv('PG_DB')}' ya existe en PostgreSQL.")

    pg_engine = create_engine(f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASS')}@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}")
    
    print("Cargando tabla 'results'...")
    pd.read_csv(archivos["results"]).to_sql('results', pg_engine, if_exists='replace', index=False)
    
    print("Cargando tabla 'races'...")
    pd.read_csv(archivos["races"]).to_sql('races', pg_engine, if_exists='replace', index=False)
    
    print("✅ PostgreSQL: Datos cargados exitosamente.")

except Exception as e:
    print(f"❌ Error en PostgreSQL: {e}")

# ==========================================
# 2. MySQL (Creación y Carga)
# ==========================================
try:
    print("\n[2/3] Configurando MySQL...")
    my_server_engine = create_engine(f"mysql+pymysql://{os.getenv('MY_USER')}:{os.getenv('MY_PASS')}@{os.getenv('MY_HOST')}:{os.getenv('MY_PORT')}/")
    
    with my_server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MY_DB')}"))
        print(f"[*] Base de datos '{os.getenv('MY_DB')}' verificada/creada en MySQL.")

    my_engine = create_engine(f"mysql+pymysql://{os.getenv('MY_USER')}:{os.getenv('MY_PASS')}@{os.getenv('MY_HOST')}:{os.getenv('MY_PORT')}/{os.getenv('MY_DB')}")
    
    print("Cargando tabla 'constructors'...")
    pd.read_csv(archivos["constructors"]).to_sql('constructors', my_engine, if_exists='replace', index=False)
    
    print("Cargando tabla 'status'...")
    pd.read_csv(archivos["status"]).to_sql('status', my_engine, if_exists='replace', index=False)
    
    print("✅ MySQL: Datos cargados exitosamente.")

except Exception as e:
    print(f"❌ Error en MySQL: {e}")

# ==========================================
# 3. MongoDB (Carga)
# ==========================================
try:
    print("\n[3/3] Configurando MongoDB...")
    mongo_client = MongoClient(os.getenv('MONGO_URI'))
    mongo_db = mongo_client["f1_source"]
    coleccion_drivers = mongo_db["drivers"]
    
    print("Limpiando colección anterior (si existe)...")
    coleccion_drivers.drop() 
    
    print("Cargando colección 'drivers'...")
    df_drivers = pd.read_csv(archivos["drivers"])
    coleccion_drivers.insert_many(df_drivers.to_dict('records'))
    
    print("✅ MongoDB: Base de datos auto-creada y datos cargados exitosamente.")

except Exception as e:
    print(f"❌ Error en MongoDB: {e}")

print("\n[INFO] Ejecución completada.")