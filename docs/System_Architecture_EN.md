# 🏛️ System Architecture - Cattle Recommender

This document describes the technical decisions and the infrastructure supporting the recommendation system.

## 1. Technology Rationale
*   **Neo4j:** Chosen for its native ability to perform graph queries in milliseconds. Unlike SQL, "Joins" here are direct relationships, allowing instant navigation through the history of thousands of farmers.
*   **Docker Compose:** Service orchestration to ensure the database and the application live in a controlled and reproducible environment.

## 2. Data Model (Property Graph)
The system is based on 4 key nodes:
*   **Farmer:** End users.
*   **Cow:** Recommendable assets.
*   **Breed & Environment:** Metadata for the content engine.

## 3. Recommendation Strategy
The system uses a hybrid architecture:
1.  **Collaborative Filtering:** Based on user similarity.
2.  **Content Filtering:** Based on cow characteristics.
3.  **Popularity:** Fallback for new users (Cold Start).

---
*Designed for scalability and low latency.*
