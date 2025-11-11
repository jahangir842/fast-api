from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Optional
import time
import asyncio

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI Basics",
    description="Learning FastAPI fundamentals",
    version="1.0.0"
)

# ============================================================================
# SECTION 1: Basic Routes & Path Operations
# ============================================================================

@app.get("/")
async def root():
    # Welcome endpoint - your first FastAPI route!
    return {
        "message": "Welcome to FastAPI Mastery!",
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/hello/{name}")
async def say_hello(name: str):
    """Path parameter example - dynamic routes"""
    return {"message": f"Hello, {name}!"}


# ============================================================================
# SYNC Example
# ============================================================================

@app.get("/slow")
def slow():
    time.sleep(5)  # blocks the server for 5 seconds
    return {"message": "Done after 5 seconds"}

# ============================================================================
# ASYNC Example
# ============================================================================

@app.get("/fast")
async def fast():
    await asyncio.sleep(5)  # non-blocking sleep
    return {"message": "Done after 5 seconds (non-blocking)"}


# ============================================================================
# SECTION 2: Path Parameters with Validation
# ============================================================================

@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1, le=1000)
):
    """
    Path parameter with validation:
    - item_id must be between 1 and 1000
    - Automatic type conversion and validation
    """
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================================================
# SECTION 3: Query Parameters
# ============================================================================

@app.get("/search")
async def search_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Query parameters with validation:
    - q: optional search query (3-50 characters)
    - skip: pagination offset (default 0)
    - limit: items per page (1-100, default 10)
    """
    results = {"query": q, "skip": skip, "limit": limit}
    return results


# ============================================================================
# SECTION 4: Request Body with Pydantic Models
# ============================================================================

class Item(BaseModel):
    """Pydantic model for request/response validation"""
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": 999.99,
                "tax": 99.99
            }
        }


@app.post("/items")
async def create_item(item: Item):
    """
    POST endpoint with request body validation
    - Automatic JSON parsing
    - Data validation via Pydantic
    - Type checking
    """
    item_dict = item.dict()
    
    # Calculate total if tax is provided
    if item.tax:
        total = item.price + item.tax
        item_dict["total"] = total
    
    return {"created": True, "item": item_dict}


# ============================================================================
# SECTION 5: Combining Path, Query, and Body Parameters
# ============================================================================

@app.put("/items/{item_id}")
async def update_item(
    item_id: int = Path(..., ge=1),
    item: Item = ...,
    q: Optional[str] = None
):
    """
    Combining all parameter types:
    - Path parameter: item_id
    - Request body: item
    - Query parameter: q
    """
    result = {"item_id": item_id, "item": item.dict()}
    if q:
        result["q"] = q
    return result


# ============================================================================
# SECTION 6: Multiple Models & Response Examples
# ============================================================================

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserInDB(User):
    """Extended model with additional fields (like hashed password)"""
    hashed_password: str


# In-memory "database" for demonstration
fake_users_db = {}


@app.post("/users", response_model=User)
async def create_user(user: User):
    """
    Create user - demonstrates response_model
    - Response will only include User fields
    - Useful for excluding sensitive data
    """
    # Simulate password hashing
    fake_hashed_password = f"hashed_{user.username}_password"
    
    # Store in "database" with hashed password
    user_in_db = UserInDB(**user.dict(), hashed_password=fake_hashed_password)
    fake_users_db[user.username] = user_in_db
    
    # Return only public user data (no hashed_password)
    return user


@app.get("/users/{username}", response_model=User)
async def get_user(username: str):
    """Get user by username - returns only public fields"""
    if username not in fake_users_db:
        return {"error": "User not found"}
    
    return fake_users_db[username]


# ============================================================================
# SECTION 7: Status Codes & Multiple Responses
# ============================================================================

from fastapi import status, HTTPException

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    DELETE endpoint with custom status code
    - Returns 204 No Content on success
    """
    # In real app, delete from database
    return None


@app.get("/items-with-error/{item_id}")
async def get_item_with_error(item_id: int):
    """
    Example of raising HTTP exceptions
    """
    if item_id > 100:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================================================
# SECTION 8: Multiple HTTP Methods on Same Path
# ============================================================================

items_db = {}

@app.get("/api/items/{item_id}")
async def api_get_item(item_id: int):
    """GET: Retrieve an item"""
    return items_db.get(item_id, {"error": "Not found"})


@app.post("/api/items/{item_id}")
async def api_create_item(item_id: int, item: Item):
    """POST: Create a new item"""
    items_db[item_id] = item.dict()
    return {"message": "Item created", "item_id": item_id}


@app.put("/api/items/{item_id}")
async def api_update_item(item_id: int, item: Item):
    """PUT: Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db[item_id] = item.dict()
    return {"message": "Item updated", "item_id": item_id}


@app.delete("/api/items/{item_id}")
async def api_delete_item(item_id: int):
    """DELETE: Remove an item"""
    if item_id in items_db:
        del items_db[item_id]
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")


# ============================================================================
# SECTION 9: Health Check Endpoint (Production Practice)
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "1.0.0"}


# ============================================================================
# Run Instructions:
# uvicorn main:app --reload
# 
# Then visit:
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)
# ============================================================================