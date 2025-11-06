from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import products_router, cart_router, orders_router
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.product import Product
from app.models.order import Order
from fastapi import Depends

app = FastAPI(title="Ecommerce API")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)

@app.get("/")
def home_page(request: Request, db: Session = Depends(get_db)):
    """Home page for customers"""
    # Get featured products (first 4 products for demo)
    featured_products = db.query(Product).limit(4).all()
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "featured_products": featured_products
    })

@app.get("/api/health")
def api_health():
    return {"ok": True, "msg": "FastAPI scaffold is running"}

# Useful redirects
@app.get("/dashboard")
def dashboard_redirect():
    """Redirect /dashboard to /admin/dashboard"""
    return RedirectResponse(url="/admin/dashboard", status_code=301)

@app.get("/admin")
def admin_redirect():
    """Redirect /admin to /admin/dashboard"""
    return RedirectResponse(url="/admin/dashboard", status_code=301)

@app.get("/products")
def products_page(request: Request, db: Session = Depends(get_db), 
                 category: str = None, search: str = None):
    """Products listing page for customers"""
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    products = query.all()
    categories = db.query(Product.category).distinct().all()
    
    return templates.TemplateResponse("shop.html", {
        "request": request,
        "products": products,
        "categories": [cat[0] for cat in categories if cat[0]],
        "current_category": category,
        "search_query": search
    })

@app.get("/product/{product_id}")
def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    """Product detail page"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        # Return 404 page or redirect
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    # Get related products (same category)
    related_products = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id
    ).limit(4).all()
    
    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "related_products": related_products
    })

@app.get("/admin/dashboard")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    # Get dashboard statistics
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    
    # Get recent orders (limit to 5)
    recent_orders = db.query(Order).order_by(Order.created_at.desc()).limit(5).all()
    
    # Calculate total revenue
    total_revenue = db.query(Order).filter(Order.status == "completed").with_entities(func.sum(Order.total_price)).scalar() or 0
    
    # Get top products (for now just get first 5 products)
    top_products = db.query(Product).limit(5).all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "top_products": top_products
    })

@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """API endpoint for real-time dashboard stats"""
    total_products = db.query(Product).count()
    total_orders = db.query(Order).count()
    pending_orders = db.query(Order).filter(Order.status == "pending").count()
    total_revenue = db.query(Order).filter(Order.status == "completed").with_entities(func.sum(Order.total_price)).scalar() or 0
    
    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "total_revenue": float(total_revenue)
    }

@app.get("/admin/products")
def admin_products(request: Request, db: Session = Depends(get_db)):
    """Products management page"""
    products = db.query(Product).all()
    return templates.TemplateResponse("products.html", {
        "request": request,
        "products": products
    })

@app.get("/admin/orders")
def admin_orders(request: Request, db: Session = Depends(get_db)):
    """Orders management page"""
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "orders": orders
    })
