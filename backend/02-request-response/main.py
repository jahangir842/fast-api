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