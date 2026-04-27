# 🛠️ Developer Guide - Cattle Recommender

This guide explains the code architecture and how to extend the recommendation system's functionalities.

## Project Structure
*   `/app/db`: Connection configuration and initialization scripts (`setup.py`).
*   `/services`: Contains `RecommendationService.py`, the brain of the application.
*   `/docs`: Technical documentation and diagrams.

## Recommendation Service
The `RecommendationService` class encapsulates all Cypher queries. Each method is designed to be independent:
*   `get_personalized_recommendations`: Implements collaborative filtering with a fallback to top-rated items.
*   `get_similar_cows`: Uses content-based similarity (Breed/Environment).

## How to add a new algorithm
1.  Define the Cypher query in a new method within `RecommendationService`.
2.  Ensure you use `$limit` or `$id` parameters to prevent injections.
3.  Update the Dashboard to consume the new method.

## Technical Requirements
*   Python 3.x
*   Neo4j Driver (`pip install neo4j`)
*   Docker & Docker Compose
