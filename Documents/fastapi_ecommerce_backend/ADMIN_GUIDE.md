# Admin API Guide

## Authentication

Admin endpoints require Bearer token authentication with the admin API key.

**Admin API Key**: `admin-super-secret-key-change-me` (configured in `.env`)

## Admin-Protected Endpoints

### Create Product
```bash
POST /products/
Authorization: Bearer admin-super-secret-key-change-me

{
  "name": "Product Name",
  "description": "Product description",
  "price": 1000,
  "stock": 50,
  "category": "electronics",
  "is_active": true
}
```

### Update Product
```bash
PUT /products/{product_id}
Authorization: Bearer admin-super-secret-key-change-me

{
  "name": "Updated Name",
  "price": 2000,
  "stock": 25
}
```

### Delete Product
```bash
DELETE /products/{product_id}
Authorization: Bearer admin-super-secret-key-change-me
```

## Public Endpoints (No Authentication Required)

- `GET /products/` - List all products
- `GET /products/{product_id}` - Get specific product
- `GET /products/debug/list` - Debug view of all products
- `GET /products/categories/list` - List all categories

## Usage in Swagger UI

1. Go to `http://localhost:8000/docs`
2. Click the "Authorize" button (🔒 icon)
3. Enter: `admin-super-secret-key-change-me`
4. Click "Authorize"
5. Now you can test admin endpoints

## Example CURL Commands

### Create a new product:
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin-super-secret-key-change-me" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "price": 80000,
    "stock": 10,
    "category": "electronics"
  }'
```

### Update a product:
```bash
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer admin-super-secret-key-change-me" \
  -d '{
    "price": 75000,
    "stock": 15
  }'
```

### Delete a product:
```bash
curl -X DELETE "http://localhost:8000/products/1" \
  -H "Authorization: Bearer admin-super-secret-key-change-me"
```

## Security Notes

- **Change the admin API key** in production (in `.env` file)
- Admin API key should be kept secret
- Regular users cannot access admin endpoints without the key
- All admin operations are logged by FastAPI
