# Module 1: FastAPI Basics

## What You'll Learn
- Creating your first FastAPI application
- Path operations (GET, POST, PUT, DELETE)
- Path parameters and query parameters
- Request bodies
- Auto-generated documentation

## Running
```bash
uvicorn main:app --reload
```

## Endpoints to Test
- GET http://localhost:8000/ - Hello World
- GET http://localhost:8000/docs - Swagger UI
- GET http://localhost:8000/items/5 - Path parameter
- GET http://localhost:8000/search?q=test - Query parameter
- POST http://localhost:8000/items - Create item

## Exercise
1. Add a DELETE endpoint for items
2. Add a PUT endpoint to update items
3. Create a new resource (e.g., users) with CRUD operations