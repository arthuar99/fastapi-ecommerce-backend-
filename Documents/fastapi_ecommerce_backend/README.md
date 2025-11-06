# 🛒 FastAPI E-commerce Backend

A complete e-commerce backend API built with FastAPI, PostgreSQL, and SQLAlchemy.

## 🌟 Features

- **Product Management**: CRUD operations for products (admin-only)
- **Shopping Cart**: Session-based cart system
- **Guest Orders**: Place orders without user registration
- **Admin Authentication**: Secure admin panel with API key authentication
- **Database Migrations**: Alembic for database schema management
- **API Documentation**: Auto-generated Swagger UI and ReDoc

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd fastapi_ecommerce_backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
```bash
cp .env.example .env
```
Edit `.env` file with your database credentials and settings.

### 5. Database Setup

#### Option A: PostgreSQL (Recommended)
```bash
# Install PostgreSQL and create database
createdb your_database_name

# Run migrations
alembic upgrade head
```

#### Option B: SQLite (Development Only)
```bash
# Update .env file:
DATABASE_URL=sqlite:///./dev.db

# Run migrations
alembic upgrade head
```

### 6. Start the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📚 API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔐 Admin Authentication

Admin endpoints require Bearer token authentication:

**Admin API Key**: Set in `.env` file as `ADMIN_API_KEY`

### Using Swagger UI:
1. Go to `http://localhost:8000/docs`
2. Click "Authorize" 🔒
3. Enter your admin API key
4. Test admin endpoints

## 🛍️ API Endpoints

### Public Endpoints (No Authentication)

#### Products
- `GET /products/` - List all products
- `GET /products/{id}` - Get product by ID
- `GET /products/categories/list` - List categories

#### Cart
- `GET /cart/` - Get current cart
- `POST /cart/items` - Add item to cart
- `PUT /cart/items/{id}` - Update cart item
- `DELETE /cart/items/{id}` - Remove cart item
- `DELETE /cart/` - Clear cart

#### Orders
- `GET /orders/` - List all orders
- `POST /orders/` - Create order from cart
- `GET /orders/{id}` - Get order details

### Admin Endpoints (Authentication Required)

#### Product Management
- `POST /products/` - Create new product
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

## 📝 Usage Examples

### Create Product (Admin)
```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-admin-key" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest iPhone model",
    "price": 80000,
    "stock": 10,
    "category": "electronics"
  }'
```

### Add to Cart (Customer)
```bash
curl -X POST "http://localhost:8000/cart/items" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### Create Order (Customer)
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "guest_name": "أحمد محمد",
    "guest_email": "ahmed@example.com",
    "guest_phone": "+201234567890"
  }'
```

## 🏗️ Project Structure

```
fastapi_ecommerce_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py            # Admin authentication
│   │   └── config.py          # Configuration
│   ├── database/
│   │   ├── __init__.py
│   │   └── session.py         # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   ├── cart.py           # Cart model
│   │   ├── cart_item.py      # Cart item model
│   │   ├── order.py          # Order models
│   │   └── product.py        # Product model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── cart.py           # Cart endpoints
│   │   ├── orders.py         # Order endpoints
│   │   └── products.py       # Product endpoints
│   └── schemas/
│       ├── __init__.py
│       ├── cart.py           # Cart schemas
│       ├── order.py          # Order schemas
│       └── product.py        # Product schemas
├── alembic/                   # Database migrations
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic configuration
├── ADMIN_GUIDE.md          # Admin usage guide
└── README.md               # This file
```

## 🔧 Development

### Adding New Migrations
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Running Tests
```bash
pytest
```

## 🌐 Frontend Integration

This backend is designed to work with any frontend framework. Key points:

### Customer Flow:
1. Browse products (`GET /products/`)
2. Add to cart (`POST /cart/items`)
3. View cart (`GET /cart/`)
4. Place order (`POST /orders/`) with guest info
5. Get order confirmation

### Admin Flow:
1. Login with admin API key
2. Manage products (CRUD operations)
3. View orders

### Authentication:
- **Customers**: No authentication required
- **Admin**: Bearer token with API key

## 🚀 Deployment

### Environment Variables (Production)
```bash
DATABASE_URL=postgresql://user:password@host:port/db
ADMIN_API_KEY=secure-random-string
DEBUG=False
```

### Docker (Optional)
```dockerfile
# Add Dockerfile for containerized deployment
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions or support, please open an issue on GitHub.

---

**Ready for frontend development!** 🎉

Your frontend developer can now:
1. Clone this repo
2. Follow the setup instructions
3. Start building the frontend using the API endpoints
4. Test everything using Swagger UI at `/docs`
# trigger workflow
