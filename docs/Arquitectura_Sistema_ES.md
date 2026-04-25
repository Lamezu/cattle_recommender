# 🏛️ Arquitectura del Sistema - Cattle Recommender

Este documento describe las decisiones técnicas y la infraestructura que soporta el sistema de recomendación.

## 1. Justificación de Tecnologías
*   **Neo4j:** Elegido por su capacidad nativa de realizar consultas de grafos en milisegundos. A diferencia de SQL, los "Joins" aquí son relaciones directas, lo que permite navegar por el historial de miles de granjeros instantáneamente.
*   **Docker Compose:** Orquestación de servicios para asegurar que la base de datos y la aplicación vivan en un entorno controlado y reproducible.

## 2. El Modelo de Datos (Property Graph)
El sistema se basa en 4 nodos clave:
*   **Farmer:** Usuarios finales.
*   **Cow:** Activos recomendables.
*   **Breed & Environment:** Metadatos para el motor de contenido.

## 3. Estrategia de Recomendación
El sistema utiliza una arquitectura híbrida:
1.  **Filtrado Colaborativo:** Basado en similitud entre usuarios.
2.  **Filtrado por Contenido:** Basado en características de la vaca.
3.  **Popularidad:** Fallback para nuevos usuarios (Cold Start).

---
*Diseñado para escalabilidad y baja latencia.*
