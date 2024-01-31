# Semantic network

A semantic network stores concepts within a graph-based data structure and accessible via an API. Each semantic network will be atomic for a specific subject, for example, a Python coding semantic network or a semantic network based on your email inbox. A Python coding semantic network may be read-only and publicly accessible while your email inbox semantic network would be read/write and private. The concepts and relationships will be added to the semantic network via an orchestrator.

# Development

1. Ensure you have [pipenv](https://pipenv.pypa.io/en/latest/) installed
2. Run `pipenv install` to install the dependencies
3. Run `pipenv shell` to shell into your environment

# Podman

Example `docker-compose.yaml`

```
version: '3'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - NEO4J_URI=neo4j://db:7687
      - NEO4J_USERNAME=neo4j
      - NEO4J_PASSWORD=superlongsecret
      - |
        API_DOCUMENTATION=API documentation
        This API is useful for answering questions about Python coding.
    depends_on:
      - db
  db:
    image: neo4j:latest
    environment:
      - NEO4J_AUTH=neo4j/superlongsecret
    ports:
      - "7687:7687"
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```

```bash
$ podman-compose up
```

# API Documentation

This API is built using Flask and Neo4j. It provides endpoints to create, read, update, delete and search nodes and relationships in a Neo4j graph database.

## Endpoints

### 1. Create Node

- **URL:** `/nodes`
- **Method:** `POST`
- **Data Params:**
  - `document` (string, required)
  - `keywords` (list of strings, required)
  - `source` (string, optional)
  - `trustworthiness` (float, required, between 0 and 1)

- **Curl Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"document":"example document", "keywords":["keyword1", "keyword2"], "trustworthiness":0.8}' http://127.0.0.1:5000/nodes
  ```

### 2. Get Node

- **URL:** `/nodes/<id>`
- **Method:** `GET`

- **Curl Example:**
  ```bash
  curl http://127.0.0.1:5000/nodes/1
  ```

### 3. Update Node

- **URL:** `/nodes/<id>`
- **Method:** `PUT`
- **Data Params:**
  - `document` (string, required)
  - `keywords` (list of strings, required)
  - `source` (string, optional)
  - `trustworthiness` (float, required, between 0 and 1)

- **Curl Example:**
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"document":"updated document", "keywords":["keyword3", "keyword4"], "trustworthiness":0.9}' http://127.0.0.1:5000/nodes/1
  ```

### 4. Delete Node

- **URL:** `/nodes/<id>`
- **Method:** `DELETE`

- **Curl Example:**
  ```bash
  curl -X DELETE http://127.0.0.1:5000/nodes/1
  ```

### 5. Search Nodes

- **URL:** `/search`
- **Method:** `GET`
- **Query Params:**
  - `query` (string, optional)
  - `keywords` (string, optional)
  - `min_trustworthiness` (float, optional, between 0 and 1)
  - `regex` (string, optional)

- **Curl Example:**
  ```bash
  curl "http://127.0.0.1:5000/search?query=example"
  curl "http://127.0.0.1:5000/search?keywords=keyword1,keyword"
  curl "http://127.0.0.1:5000/search?min_trustworthiness=0.7"
  curl "http://127.0.0.1:5000/search?regex=ex.*le"
  ```

 Multiple arguments are joined with AND conditions

  ```bash
  curl "http://127.0.0.1:5000/search?query=example&keywords=keyword1"
  curl "http://127.0.0.1:5000/search??regex=ex.*le&min_trustworthiness=0.7"
  ```

### 6. Create Relationship

- **URL:** `/nodes/<id>/relationships`
- **Method:** `POST`
- **Data Params:**
  - `target_id` (integer, required)
  - `weight` (float, required, between 0 and 1)

- **Curl Example:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"target_id":2, "weight":0.5}' http://127.0.0.1:5000/nodes/1/relationships
  ```

### 7. Get Relationships

- **URL:** `/nodes/<id>/relationships`
- **Method:** `GET`

- **Curl Example:**
  ```bash
  curl http://127.0.0.1:5000/nodes/1/relationships
  ```

### 8. Delete Relationship

- **URL:** `/relationships/<id>`
- **Method:** `DELETE`

- **Curl Example:**
  ```bash
  curl -X DELETE http://127.0.0.1:5000/relationships/1
  ```

### 9. Get Documentation

- **URL:** `/documentation`
- **Method:** `GET`

- **Curl Example:**
  ```bash
  curl http://127.0.0.1:5000/documentation
  ```

### 10. Delete All Nodes and Relationships

- **URL:** `/delete_all`
- **Method:** `DELETE`

- **Curl Example:**
  ```bash
  curl -X DELETE http://127.0.0.1:5000/delete_all
  ```