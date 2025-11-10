# FastAPI Mastery - Complete Starter Code

I'll provide the complete code for all phases. Let's start!

## Project Setup

### Root Files

**`README.md`**
```markdown
# FastAPI Mastery: From Scratch to Production

A comprehensive learning repository for mastering FastAPI with React + Vite frontend.

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Modules

Each module is self-contained. Navigate to the module folder and run:

```bash
cd 01-basics
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs for interactive API documentation

## Learning Path

1. **01-basics** - FastAPI fundamentals
2. **02-request-response** - Advanced request/response handling
3. **03-validation** - Pydantic validation deep dive
4. **04-database** - SQLAlchemy integration
5. **05-authentication** - JWT authentication & security
6. **06-file-handling** - File uploads/downloads
7. **07-websockets** - Real-time communication
8. **08-testing** - Comprehensive testing
9. **09-deployment** - Docker & production deployment
10. **10-fullstack-project** - Complete full-stack application

## Progress Tracking

- [ ] Complete 01-basics
- [ ] Complete 02-request-response
- [ ] Complete 03-validation
- [ ] Complete 04-database
- [ ] Complete 05-authentication
- [ ] Complete 06-file-handling
- [ ] Complete 07-websockets
- [ ] Complete 08-testing
- [ ] Complete 09-deployment
- [ ] Complete 10-fullstack-project
```

**`requirements.txt`**
```txt
# Core FastAPI
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy==2.0.25
alembic==1.13.1
aiosqlite==0.19.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
httpx==0.26.0

# Utilities
python-dotenv==1.0.0
pillow==10.2.0

# WebSockets
websockets==12.0

# CORS
```

**`.gitignore`**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# FastAPI
.env
*.db
*.sqlite3

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Node (for frontend)
node_modules/
dist/
.env.local
```

---

## Phase 1: Foundation

### Module 1: FastAPI Basics

**`01-basics/README.md`**
```markdown
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
```

**`01-basics/main.py`**
```python
from fastapi import FastAPI, Path, Query
from pydantic import BaseModel
from typing import Optional

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
    """Welcome endpoint - your first FastAPI route!"""
    return {
        "message": "Welcome to FastAPI Mastery!",
        "docs": "Visit /docs for interactive API documentation"
    }

@app.get("/hello/{name}")
async def say_hello(name: str):
    """Path parameter example - dynamic routes"""
    return {"message": f"Hello, {name}!"}


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
```

---

### Module 2: Request & Response Handling

**`02-request-response/README.md`**
```markdown
# Module 2: Advanced Request & Response Handling

## What You'll Learn
- Response models and status codes
- Custom headers and cookies
- Different response types (JSON, HTML, File, etc.)
- Response validation
- Dependency injection basics

## Running
```bash
uvicorn main:app --reload
```

## Key Concepts
- **Response Model**: Control what data is returned
- **Status Codes**: Proper HTTP status code usage
- **Headers**: Custom response headers
- **Cookies**: Setting and reading cookies

## Exercise
1. Create an endpoint that returns different response types based on query param
2. Implement a logout endpoint that clears cookies
3. Add custom headers to track API version
```

**`02-request-response/main.py`**
```python
from fastapi import FastAPI, Response, status, Header, Cookie, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, FileResponse, StreamingResponse, RedirectResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union
from datetime import datetime
import io

app = FastAPI(title="Request & Response Mastery", version="2.0.0")

# ============================================================================
# SECTION 1: Response Models & Field Exclusion
# ============================================================================

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    """Public user data - password excluded"""
    id: int
    created_at: datetime
    is_active: bool = True


class UserInDB(UserResponse):
    """Internal model with sensitive data"""
    hashed_password: str


# Fake database
users_db = {}
user_id_counter = 1


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create user with response_model to exclude password
    - Input includes password
    - Output excludes password (security!)
    """
    global user_id_counter
    
    # Simulate password hashing
    hashed_password = f"hashed_{user.password}"
    
    # Create user in DB
    user_in_db = UserInDB(
        id=user_id_counter,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        created_at=datetime.now(),
        hashed_password=hashed_password
    )
    
    users_db[user_id_counter] = user_in_db
    user_id_counter += 1
    
    return user_in_db


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user - automatically excludes hashed_password"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


# ============================================================================
# SECTION 2: Multiple Response Models
# ============================================================================

class ItemBase(BaseModel):
    name: str
    price: float


class ItemPublic(ItemBase):
    """Public item data"""
    id: int


class ItemDetail(ItemPublic):
    """Detailed item with additional fields"""
    description: str
    stock: int
    created_at: datetime


@app.get("/items/{item_id}", response_model=Union[ItemPublic, ItemDetail])
async def get_item(item_id: int, detailed: bool = False):
    """
    Return different response models based on query parameter
    - Simple view vs detailed view
    """
    base_item = {
        "id": item_id,
        "name": f"Item {item_id}",
        "price": 99.99
    }
    
    if detailed:
        return ItemDetail(
            **base_item,
            description="Detailed description",
            stock=50,
            created_at=datetime.now()
        )
    
    return ItemPublic(**base_item)


# ============================================================================
# SECTION 3: Custom Status Codes & Headers
# ============================================================================

@app.post("/items-custom", status_code=status.HTTP_201_CREATED)
async def create_item_custom(item: ItemBase, response: Response):
    """
    Custom status code and headers
    - Set custom headers in response
    - Return 201 Created
    """
    response.headers["X-Custom-Header"] = "CustomValue"
    response.headers["X-Item-Id"] = "12345"
    
    return {"message": "Item created", "item": item.dict()}


@app.get("/items-conditional/{item_id}")
async def get_item_conditional(item_id: int, response: Response):
    """
    Conditional status codes
    - Return different status codes based on conditions
    """
    if item_id > 100:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "Item not found"}
    
    response.status_code = status.HTTP_200_OK
    return {"item_id": item_id, "name": f"Item {item_id}"}


# ============================================================================
# SECTION 4: Reading Headers
# ============================================================================

@app.get("/read-headers")
async def read_headers(
    user_agent: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    x_custom_header: Optional[str] = Header(None)
):
    """
    Read request headers
    - FastAPI converts header names: X-Custom-Header -> x_custom_header
    """
    return {
        "user_agent": user_agent,
        "accept_language": accept_language,
        "custom_header": x_custom_header
    }


# ============================================================================
# SECTION 5: Cookies
# ============================================================================

@app.post("/login")
async def login(username: str, password: str, response: Response):
    """
    Login endpoint that sets cookie
    - In production, validate credentials and use secure JWT
    """
    if username == "admin" and password == "secret":
        response.set_cookie(
            key="session_token",
            value=f"token_{username}",
            httponly=True,  # Prevent JavaScript access
            max_age=3600,   # 1 hour
            samesite="lax"  # CSRF protection
        )
        return {"message": "Logged in successfully"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/profile")
async def get_profile(session_token: Optional[str] = Cookie(None)):
    """
    Protected endpoint that reads cookie
    """
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # In production, validate token
    return {"message": "Profile data", "token": session_token}


@app.post("/logout")
async def logout(response: Response):
    """
    Logout endpoint that clears cookie
    """
    response.delete_cookie("session_token")
    return {"message": "Logged out successfully"}


# ============================================================================
# SECTION 6: Different Response Types
# ============================================================================

@app.get("/html", response_class=HTMLResponse)
async def get_html():
    """Return HTML response"""
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI HTML Response</title>
        </head>
        <body>
            <h1>Hello from FastAPI!</h1>
            <p>This is an HTML response</p>
        </body>
    </html>
    """
    return html_content


@app.get("/text", response_class=PlainTextResponse)
async def get_text():
    """Return plain text response"""
    return "This is a plain text response"


@app.get("/custom-json")
async def get_custom_json():
    """
    Custom JSON response with additional headers
    """
    content = {"message": "Custom JSON", "timestamp": datetime.now().isoformat()}
    return JSONResponse(
        content=content,
        headers={"X-Custom": "Value"},
        status_code=200
    )


@app.get("/redirect")
async def redirect_example():
    """Redirect to another endpoint"""
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


# ============================================================================
# SECTION 7: File Responses
# ============================================================================

@app.get("/download-file")
async def download_file():
    """
    Return a file for download
    Note: In production, serve actual files
    """
    # Create a sample file in memory
    content = "This is sample file content\nLine 2\nLine 3"
    
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": "attachment; filename=sample.txt"}
    )


@app.get("/stream")
async def stream_response():
    """
    Stream response - useful for large files
    """
    def generate():
        for i in range(10):
            yield f"Chunk {i}\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )


# ============================================================================
# SECTION 8: Dependency Injection Basics
# ============================================================================

def get_query_params(skip: int = 0, limit: int = 10):
    """Reusable dependency for pagination"""
    return {"skip": skip, "limit": limit}


def verify_token(x_token: str = Header(...)):
    """Reusable dependency for authentication"""
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token


@app.get("/items-with-deps")
async def get_items_with_deps(
    pagination: dict = Depends(get_query_params),
    token: str = Depends(verify_token)
):
    """
    Using dependencies for:
    - Pagination parameters
    - Authentication
    """
    return {
        "message": "Items retrieved",
        "pagination": pagination,
        "authenticated": True
    }


# ============================================================================
# SECTION 9: Response Model with List
# ============================================================================

@app.get("/users", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    """
    Return list of users with response model
    """
    users_list = list(users_db.values())[skip:skip + limit]
    return users_list


# ============================================================================
# SECTION 10: Exclude/Include Fields Dynamically
# ============================================================================

class Product(BaseModel):
    name: str
    price: float
    description: str
    internal_code: str
    stock: int


@app.get("/products/{product_id}")
async def get_product(product_id: int, include_internal: bool = False):
    """
    Dynamically exclude/include fields
    """
    product = Product(
        name="Laptop",
        price=999.99,
        description="Gaming laptop",
        internal_code="INT-12345",
        stock=50
    )
    
    if include_internal:
        return product
    
    # Exclude internal fields
    return product.dict(exclude={"internal_code"})


# ============================================================================
# Run: uvicorn main:app --reload
# Visit: http://localhost:8000/docs
# ============================================================================
```

Would you like me to continue with **Module 3 (Validation)** and beyond? I'll provide all 10 modules with complete, production-ready code!