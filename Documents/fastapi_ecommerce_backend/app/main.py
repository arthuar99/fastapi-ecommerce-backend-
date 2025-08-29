from fastapi import FastAPI
from app.routers import products_router, cart_router, orders_router

app = FastAPI(title="Ecommerce API")

# Include routers
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)

@app.get("/")
def root():
    return {"ok": True, "msg": "FastAPI scaffold is running"}
