# Justificación: Script de Inicialización de Restricciones en Neo4j (`setup.py`)

## Contexto del Cambio
Durante la fase de diseño del **Modelo de Grafo** para el Sistema de Recomendación de Vacas, se identificó la necesidad de añadir un paso previo no contemplado originalmente en la planificación diaria: **La creación de restricciones de unicidad (Constraints)** en Neo4j antes de la ingesta de datos.

Para ello, se propuso la creación de un pequeño script de inicialización (`app/db/setup.py`).

## ¿Por qué es necesario este script?

Aunque Neo4j es una base de datos "schemaless" (sin esquema rígido) que permite insertar nodos al vuelo, un **Sistema de Recomendación en producción** requiere integridad y velocidad. Este script cumple dos funciones críticas:

### 1. Integridad de los Datos (Evitar Duplicados)
Al importar miles de datos (generados por Sara), existe el riesgo de que por un fallo de red o doble ejecución se inserten dos nodos con el mismo ID. 
- Si tuviéramos dos nodos `Farmer` con `farmer_id: F0001`, las consultas de recomendación sumarían relaciones duplicadas, arrojando resultados falsos o sobreestimados.
- Las `CONSTRAINTS` impiden físicamente que se creen duplicados en la base de datos, garantizando la fiabilidad del recomendador.

### 2. Rendimiento y Optimización (Índices Implícitos)
En Neo4j, crear una restricción de unicidad (`IS UNIQUE`) **crea automáticamente un índice (B-Tree)** sobre esa propiedad.
- **Sin índice:** Para encontrar a la vaca `C0120` al registrar una compra, Neo4j tiene que escanear todas las vacas una por una: **O(n)**.
- **Con índice:** Neo4j va directamente a la vaca usando un árbol de búsqueda: **O(log n)**.
- Al tener índices en `farmer_id`, `cow_id`, `breed.name` y `environment.type`, las consultas del recomendador que busquen un punto de partida (ej. *"Dado el granjero F005..."*) se ejecutarán en milisegundos en lugar de segundos.

## Cómo defenderlo en la Demo o ante el Profesor
Si preguntan por qué se añadió este paso extra, la defensa técnica ideal es:

> *"Decidimos añadir un paso de inicialización de Constraints en Neo4j de forma proactiva. Nos dimos cuenta de que, sin restricciones de unicidad en los IDs, nos exponíamos a duplicidad de nodos durante la importación masiva de datos, lo que corrompería las recomendaciones. Además, esta decisión arquitectónica nos regala la creación de índices subyacentes, bajando el coste computacional de nuestras búsquedas de O(n) a O(log n), algo indispensable para un algoritmo de recomendación eficiente."*

## Siguientes Pasos
Este script se ejecutará una única vez antes de que el pipeline de datos (Dataset) a cargo de Sara importe los nodos. Una vez establecido, el modelo es seguro para empezar a recibir relaciones `BUYS`, `VIEWED` y `RATED` y poder construir las consultas de recomendación.
