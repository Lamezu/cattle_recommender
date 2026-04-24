from neo4j import GraphDatabase
from app.db.setup import setup_database_constraints

def run_setup():
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "password"

    print("--- Iniciando configuración de la Base de Datos ---")
    
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        
        # Verificamos la conexión
        driver.verify_connectivity()
        print("[✓] Conexión establecida con Neo4j local.")

        # Ejecutamos las restricciones que diseñó Alejandro
        print("[...] Aplicando restricciones de unicidad e índices...")
        setup_database_constraints(driver)
        print("[✓] Restricciones aplicadas correctamente.")
        
        driver.close()
        print("--- Configuración finalizada con éxito ---")
        print("\nYa puedes ir al navegador (localhost:7474) y escribir ':schema' para verlas.")

    except Exception as e:
        print(f"[X] Error al conectar o configurar la base de datos: {e}")

if __name__ == "__main__":
    run_setup()
