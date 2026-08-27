import kagglehub
import shutil
import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

print("Iniciando descarga del dataset de F1...")

ruta_cache = kagglehub.dataset_download("rohanrao/formula-1-world-championship-1950-2020")
print("Descarga completada. Filtrando archivos...")

carpeta_destino = "./datasets/kaggle_f1"
archivos_requeridos = [
    "results.csv",
    "races.csv",
    "constructors.csv",
    "status.csv",
    "drivers.csv",
    "circuits.csv"
]

if os.path.exists(carpeta_destino):
    shutil.rmtree(carpeta_destino)
os.makedirs(carpeta_destino, exist_ok=True)

archivos_copiados = 0
for archivo in os.listdir(ruta_cache):
    if archivo in archivos_requeridos:
        ruta_origen = os.path.join(ruta_cache, archivo)
        ruta_final = os.path.join(carpeta_destino, archivo)
        
        shutil.copy(ruta_origen, ruta_final)
        archivos_copiados += 1
        print(f"✅ Copiado: {archivo}")

print(f"\nSe copiaron {archivos_copiados} archivos a la carpeta '{carpeta_destino}'.")