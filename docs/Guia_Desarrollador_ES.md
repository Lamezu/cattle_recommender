# 🛠️ Guía del Desarrollador - Cattle Recommender

Esta guía explica la arquitectura del código y cómo extender las funcionalidades del sistema de recomendación.

## Estructura del Proyecto
*   `/app/db`: Configuración de la conexión y scripts de inicialización (`setup.py`).
*   `/services`: Contiene el `RecommendationService.py`, el cerebro de la aplicación.
*   `/docs`: Documentación técnica y diagramas.

## El Servicio de Recomendación
La clase `RecommendationService` encapsula todas las consultas Cypher. Cada método está diseñado para ser independiente:
*   `get_personalized_recommendations`: Implementa filtrado colaborativo con un fallback a las mejor valoradas.
*   `get_similar_cows`: Utiliza similitud basada en contenido (Breed/Environment).

## Cómo añadir un nuevo algoritmo
1.  Defina la consulta Cypher en un nuevo método dentro de `RecommendationService`.
2.  Asegúrese de usar parámetros `$limit` o `$id` para evitar inyecciones.
3.  Actualice el Dashboard para consumir el nuevo método.

## Requisitos Técnicos
*   Python 3.x
*   Driver de Neo4j (`pip install neo4j`)
*   Docker & Docker Compose
