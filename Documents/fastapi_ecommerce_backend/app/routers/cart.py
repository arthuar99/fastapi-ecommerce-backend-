from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.schemas.cart import CartItemCreate, CartItemUpdate, Cart as CartSchema, CartItem as CartItemSchema

router = APIRouter(prefix="/cart", tags=["cart"])


def get_or_create_cart(db: Session, session_id: str = "default") -> Cart:
    """Get existing cart or create new one for session"""
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=CartSchema)
def get_cart(session_id: str = "default", db: Session = Depends(get_db)):
    """Get current cart with items and totals"""
    cart = get_or_create_cart(db, session_id)
    
    # Get cart items with product details
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    
    # Calculate totals
    total_items = sum(item.quantity for item in cart_items)
    total_price = 0
    
    # Get product details for each item
    items_with_details = []
    for item in cart_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            item_total = product.price * item.quantity
            total_price += item_total
            
            items_with_details.append({
                "id": item.id,
                "cart_id": item.cart_id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_name": product.name,
                "product_price": product.price,
                "total_price": item_total
            })
    
    return {
        "id": cart.id,
        "items": items_with_details,
        "total_items": total_items,
        "total_price": total_price
    }


@router.post("/items", response_model=CartItemSchema)
def add_to_cart(
    item_data: CartItemCreate, 
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    """Add item to cart"""
    # Check if product exists
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {item_data.product_id} not found"
        )
    
    # Check if product is active
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{product.name}' is not available for purchase"
        )
    
    # Check stock availability (only if stock is tracked)
    if hasattr(product, 'stock') and product.stock is not None:
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}, Requested: {item_data.quantity}"
            )
    
    cart = get_or_create_cart(db, session_id)
    
    # Check if item already exists in cart
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item_data.quantity
        
        # Check stock for total quantity
        if hasattr(product, 'stock') and product.stock is not None:
            if product.stock < new_quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock for total quantity. Available: {product.stock}, Total requested: {new_quantity}"
                )
        
        existing_item.quantity = new_quantity
        db.commit()
        db.refresh(existing_item)
        
        # Return enriched data with product details
        return {
            "id": existing_item.id,
            "cart_id": existing_item.cart_id,
            "product_id": existing_item.product_id,
            "quantity": existing_item.quantity,
            "product_name": product.name,
            "product_price": product.price,
            "total_price": product.price * existing_item.quantity
        }
    else:
        # Add new item
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        
        # Return enriched data with product details
        return {
            "id": cart_item.id,
            "cart_id": cart_item.cart_id,
            "product_id": cart_item.product_id,
            "quantity": cart_item.quantity,
            "product_name": product.name,
            "product_price": product.price,
            "total_price": product.price * cart_item.quantity
        }


@router.put("/items/{item_id}", response_model=CartItemSchema)
def update_cart_item(
    item_id: int, 
    item_data: CartItemUpdate,
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    """Update cart item quantity"""
    cart = get_or_create_cart(db, session_id)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Check stock availability
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if product and hasattr(product, 'stock') and product.stock is not None:
        if product.stock < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Available: {product.stock}"
            )
    
    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(
    item_id: int,
    session_id: str = "default",
    db: Session = Depends(get_db)
):
    """Remove item from cart"""
    cart = get_or_create_cart(db, session_id)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    db.delete(cart_item)
    db.commit()
    return None


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart(session_id: str = "default", db: Session = Depends(get_db)):
    """Clear all items from cart"""
    cart = get_or_create_cart(db, session_id)
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return None
