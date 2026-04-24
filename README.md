# 🐄 Cattle Recommender System - Proyecto AED

Sistema inteligente de recomendación de ganado basado en grafos (Neo4j) y Python. Diseñado para optimizar la toma de decisiones de granjeros mediante algoritmos colaborativos y basados en contenido.

---

## 🚀 Stack Tecnológico
*   **Database:** Neo4j (Graph Database)
*   **Backend:** Python 3.x
*   **Containerization:** Docker
*   **Logic:** Cypher Query Language

## 📊 Modelo de Grafo
El sistema utiliza una arquitectura de grafos para conectar granjeros con vacas basándose en su comportamiento y características.

![Esquema del Grafo](docs/diagrams/graph_model_schema.png)

### Nodos Principales
*   **Farmer:** Identidad del usuario.
*   **Cow:** El activo principal con atributos de raza, precio y valoración.
*   **Breed & Environment:** Contexto para recomendaciones por contenido.

---

## 🛠️ Configuración del Entorno

### 1. Base de Datos (Docker)
Para levantar el entorno local de Neo4j:
```powershell
docker run --name neo4j-cattle -p 7474:7474 -p 7687:7687 -d -e NEO4J_AUTH=neo4j/password neo4j:latest
```

### 2. Inicialización del Esquema
Es necesario configurar las restricciones de unicidad e índices antes de la carga de datos:
```powershell
python3 -m pip install neo4j
python3 test_db.py
```

---

## 📚 Documentación
*Próximamente disponibles los manuales completos en el directorio `/docs`:*

| Documento | Idioma | Versión |
| :--- | :--- | :--- |
| **Guía de Usuario** | 🇪🇸 Español / 🇬🇧 English | v1.0 |
| **Guía del Desarrollador** | 🇪🇸 Español / 🇬🇧 English | v1.0 |
| **Justificación de Base de Datos** | 🇪🇸 Español | [Ver aquí](docs/db_setup_explanation.md) |

---

## 👥 Equipo
*   **Alejandro:** Modelo de Grafo y Lógica de Recomendación.
*   **Samuel:** Infraestructura Backend y Conexión.
*   **Sara:** Generación de Datasets y Coherencia de Datos.
