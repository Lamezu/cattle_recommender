# 🐄 Cattle Recommender System - AED Project

Intelligent cattle recommendation system based on graphs (Neo4j) and Python. Designed to optimize farmer decision-making through collaborative and content-based algorithms.

---

## 🚀 Tech Stack
*   **Database:** Neo4j (Graph Database)
*   **Backend:** Python 3.x
*   **Containerization:** Docker
*   **Logic:** Cypher Query Language

## 📐 Architecture and Flows
Detailed visualization of the data structure and user experience.

### 1. Graph Model
Definition of nodes and relationships in Neo4j.
![Graph Schema](docs/diagrams/graph_model_schema.svg)

### 2. User Flow (Farmer Journey)
The path the farmer takes from Login to receiving recommendations.
![User Flow](docs/diagrams/cow_app_flow_for_farmers.svg)

### 3. Recommendation Logic (The Brain)
Algorithms applied to generate the lists for each tab.
![Recommendation Logic](docs/diagrams/recommendations_system.svg)

---

## 🛠️ Environment Setup

### 1. Database (Docker)
To start the local Neo4j environment:
```powershell
docker run --name neo4j-cattle -p 7474:7474 -p 7687:7687 -d -e NEO4J_AUTH=neo4j/password neo4j:latest
```

### 2. Schema Initialization
Uniqueness constraints and indexes must be configured before data loading:
```powershell
python3 -m pip install neo4j
python3 test_db.py
```

---

## 📚 Documentation
*Complete manuals available in the `/docs` directory:*

| Document | Language | Link |
| :--- | :--- | :--- |
| **User Guide** | 🇬🇧 English | [See here](docs/User_Guide_EN.md) |
| **Guía de Usuario** | 🇪🇸 Español | [See here](docs/Guia_Usuario_ES.md) |
| **Developer Guide** | 🇬🇧 English | [See here](docs/Developer_Guide_EN.md) |
| **Guía del Desarrollador** | 🇪🇸 Español | [See here](docs/Guia_Desarrollador_ES.md) |
| **Architecture** | 🇬🇧 English | [See here](docs/System_Architecture_EN.md) |
| **Arquitectura** | 🇪🇸 Español | [See here](docs/Arquitectura_Sistema_ES.md) |

---

## 👥 Team
*   **Alejandro:** Graph Model and Recommendation Logic.
*   **Samuel:** Backend Infrastructure and Connection.
*   **Sara:** Dataset Generation and Data Consistency.
