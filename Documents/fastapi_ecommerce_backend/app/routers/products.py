from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, Product as ProductSchema
from app.core.auth import admin_required

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductSchema])
def get_products(
    skip: int = 0, 
    limit: int = 100, 
    category: str = None,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """List all products with optional filtering"""
    query = db.query(Product)
    
    if active_only:
        query = query.filter(Product.is_active == True)
    
    if category:
        query = query.filter(Product.category == category)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/debug/list")
def debug_products(db: Session = Depends(get_db)):
    """Debug endpoint to see all products with their IDs"""
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock,
            "is_active": p.is_active,
            "category": p.category
        }
        for p in products
    ]


@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db), _: bool = admin_required):
    """Create new product"""
    # Check if product with same name already exists
    existing_product = db.query(Product).filter(Product.name == product_data.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )
    
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db), _: bool = admin_required):
    """Update product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if new name conflicts with existing product
    if product_data.name and product_data.name != product.name:
        existing_product = db.query(Product).filter(Product.name == product_data.name).first()
        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this name already exists"
            )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), _: bool = admin_required):
    """Delete product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None


@router.get("/categories/list")
def get_categories(db: Session = Depends(get_db)):
    """Get list of all product categories"""
    categories = db.query(Product.category).distinct().filter(Product.category.isnot(None)).all()
    return [category[0] for category in categories]
