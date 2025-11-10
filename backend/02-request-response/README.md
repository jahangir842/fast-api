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