# FastAPI Quick Reference Guide

A quick reference guide for building REST APIs with FastAPI.

## Installation

```bash
pip install fastapi
pip install "uvicorn[standard]"
```

## Basic API Structure

```python
from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Basic GET route
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Path parameters
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# Query parameters
@app.get("/search/")
async def search_items(q: str, skip: int = 0, limit: int = 10):
    return {"query": q, "skip": skip, "limit": limit}
```

## Request Body Models

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    disabled: bool = False

@app.post("/users/")
async def create_user(user: User):
    return user
```

## Common HTTP Methods

```python
# GET - Fetch data
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # ... fetch user from database
    return {"user_id": user_id}

# POST - Create new resource
@app.post("/users/")
async def create_user(user: User):
    # ... save user to database
    return user

# PUT - Update entire resource
@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    # ... update user in database
    return user

# PATCH - Partial update
@app.patch("/users/{user_id}")
async def partial_update(user_id: int, user: User):
    # ... partially update user
    return user

# DELETE - Remove resource
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    # ... delete user from database
    return {"status": "deleted"}
```

## Path Parameters with Validation

```python
@app.get("/users/{user_id}")
async def read_user(
    user_id: int = Path(..., title="User ID", ge=1, description="ID of the user to fetch")
):
    return {"user_id": user_id}
```

## Query Parameters with Validation

```python
@app.get("/items/")
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    q: Optional[str] = Query(None, min_length=3, max_length=50)
):
    return {"skip": skip, "limit": limit, "q": q}
```

## Error Handling

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in database:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": database[user_id]}
```

## Dependencies

```python
from fastapi import Depends

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
async def read_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items
```

## Authentication Example

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": create_access_token(user), "token_type": "bearer"}

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Running the Server

```bash
# Development server
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 80
```

## Automatic Documentation

FastAPI automatically generates API documentation:
- Interactive API docs: `/docs` (Swagger UI)
- Alternative API docs: `/redoc` (ReDoc)

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## File Upload Example

```python
from fastapi import File, UploadFile

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def write_notification(email: str, message=""):
    with open("log.txt", mode="a") as email_file:
        content = f"notification for {email}: {message}\n"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

## Response Models

```python
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item

@app.get("/items/", response_model=List[Item])
async def list_items():
    return [
        {"name": "Foo", "price": 42},
        {"name": "Bar", "price": 21}
    ]
```

## Best Practices

1. Use Pydantic models for request/response validation
2. Implement proper error handling
3. Use async functions for I/O-bound operations
4. Implement proper authentication/authorization
5. Use dependency injection for database connections
6. Document your API endpoints
7. Implement rate limiting for production
8. Use environment variables for configuration
9. Implement logging
10. Write tests for your API endpoints

## Testing FastAPI Applications

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 42},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"
```