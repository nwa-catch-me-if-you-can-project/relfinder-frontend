### API

The application requires an API with two endpoints:

```sh
GET /entities
```

This endpoint should return a list of all entities in the knowledge graph as a `json` object with the following format:

```json
{
    "entities" [{
        "id": "Entity-1234",             // The identifier used in the knowledge graph
        "name": "Lorem Dolor LLC"        // The human readable entity name
    }]
}
```

---

```sh
GET /query
```

This endpoint should return a graph containing the queried entities and the relationships between them. It should accept a `json` body in the following format:

```json
{
    // A list of entities identified by their knowledge graph ID
    "entities": ["Entity-1234", ...]
}
```

And return a `json` response in a format similar to the one discussed in the _Application data representation_ section.

### Application data representation

The application represents the knowledge graph using the following data structure.

```json
{
    "nodes: [{
        "id": 0,                                // A progressive integer ID
        "name": "Lorem Dolor LLC",              // The entity's name
        "class": "AcquiringCompany"             // The entity's class
    }, {
        "id": 1,
        "name": "ACME Sarl",
        "class": "MergingCompany"
    }, ...],
    "edges": [{
        "sid": 0,                               // The source node ID
        "tid": 1,                               // The destination node ID
        "name": "acquires",                     // The property name
    }, ...],
    "classes": [{                               // List of all classes in the graph
        "class": "AcquiringCompany",
        "color": "#e291e2"
    }, {
        "class": "MergingCompany",
        "color": "#f201e8"
    }]
}
```