# 📑 Guía Maestra de Consultas Cypher - Cattle Recommender

Esta guía explica cómo formular consultas en la base de datos Neo4j para extraer información valiosa y entender los algoritmos de recomendación implementados.

## 1. Fundamentos de Cypher
Cypher es un lenguaje declarativo basado en patrones visuales:
- `()` representa un **Nodo**.
- `[]` representa una **Relación**.
- `{}` contiene las **Propiedades**.
- `->` indica la **Dirección** del flujo.

### Ejemplo Básico:
```cypher
MATCH (f:Farmer {name: 'Victor'})-[:BUYS]->(c:Cow)
RETURN c.name, c.price
```
*Traducción: Busca al granjero Victor, mira qué vacas ha comprado y devuélveme sus nombres y precios.*

---

## 2. Consultas de Auditoría (Estado del Sistema)
Útiles para verificar que los datos se han cargado correctamente.

- **Contar nodos por tipo:**
```cypher
MATCH (n) RETURN labels(n) as Tipo, count(n) as Total
```

- **Ver las vacas con mejores valoraciones:**
```cypher
MATCH (c:Cow)<-[r:RATED]-(:Farmer)
RETURN c.name as Vaca, avg(r.stars) as Media, count(r) as Votos
ORDER BY Media DESC, Votos DESC
LIMIT 10
```

---

## 3. Lógica de Recomendación (El Cerebro)

### A. Filtrado Colaborativo (User-User)
**Concepto:** "Si al granjero A le gusta lo mismo que al granjero B, lo que compre B le gustará a A".

> **Nota para el navegador:** Reemplaza `$id` por un ID real (ej: `'F0001'`) o define el parámetro con `:param id: 'F0001'`.

```cypher
MATCH (yo:Farmer {farmer_id: $id})-[:BUYS]->(comun:Cow)<-[:BUYS]-(otro:Farmer)
MATCH (otro)-[:BUYS]->(recomendacion:Cow)
WHERE yo <> otro AND NOT (yo)-[:BUYS]->(recomendacion)
RETURN recomendacion.name, count(otro) as Peso
ORDER BY Peso DESC
```

### B. Similitud por Contenido (Item-Item)
**Concepto:** "Busca vacas que compartan la misma Raza y vivan en el mismo Entorno que la vaca que estoy mirando".
```cypher
MATCH (vaca_actual:Cow {cow_id: $id})-[:HAS_BREED|LIVES_IN]->(caracteristica)
MATCH (caracteristica)<-[:HAS_BREED|LIVES_IN]-(vaca_sugerida:Cow)
WHERE vaca_actual <> vaca_sugerida
RETURN vaca_sugerida.name, count(caracteristica) as Coincidencias
ORDER BY Coincidencias DESC
```

---

## 4. Consejos para la Defensa
- **Relaciones vs Joins:** Explica que en Neo4j no hay tablas, por lo que buscar recomendaciones es instantáneo ya que solo seguimos "flechas" (punteros), no comparamos miles de filas.
- **Filtros Direccionales:** Siempre usa `->` para indicar quién interactúa con quién.
- **Agregaciones:** Usa `count()` para medir popularidad y `avg()` para calidad.

---
*Documento generado para el Proyecto AED - Cattle Recommender*
