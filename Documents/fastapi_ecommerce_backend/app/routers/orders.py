from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.session import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.schemas.order import OrderCreate, Order as OrderSchema, OrderSummary, OrderItem as OrderItemSchema

router = APIRouter(prefix="/orders", tags=["orders"])


def get_or_create_cart(db: Session, session_id: str = "default") -> Cart:
    """Get existing cart or create new one for session"""
    cart = db.query(Cart).filter(Cart.session_id == session_id).first()
    if not cart:
        cart = Cart(session_id=session_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=List[OrderSummary])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all orders (admin only) - paginated"""
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get order details by ID"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.post("/", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
def create_order(order_data: OrderCreate, session_id: str = "default", db: Session = Depends(get_db)):
    """Create order from cart with guest information"""
    # Get the current cart for the session
    cart = get_or_create_cart(db, session_id)
    
    # Check if cart has items
    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot create order from empty cart"
        )
    
    # Create the order
    order = Order(
        guest_name=order_data.guest_name,
        guest_email=order_data.guest_email,
        guest_phone=order_data.guest_phone
    )
    db.add(order)
    db.flush()  # Get the order ID
    
    # Create order items from cart items
    total_price = 0
    total_items = 0
    
    for cart_item in cart_items:
        # Get product details
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {cart_item.product_id} not found"
            )
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity
        )
        db.add(order_item)
        
        # Calculate totals
        item_total = product.price * cart_item.quantity
        total_price += item_total
        total_items += cart_item.quantity
    
    # Update order totals
    order.total_price = total_price
    order.total_items = total_items
    
    # Clear the cart after successful order creation
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    
    # Commit the transaction
    db.commit()
    db.refresh(order)
    
    # Get order items with product details for response
    order_items_with_details = []
    for order_item in order.items:
        product = db.query(Product).filter(Product.id == order_item.product_id).first()
        if product:
            order_items_with_details.append({
                "id": order_item.id,
                "order_id": order_item.order_id,
                "product_id": order_item.product_id,
                "quantity": order_item.quantity,
                "product_name": product.name,
                "product_price": product.price,
                "total_price": product.price * order_item.quantity
            })
    
    # Return enriched order data
    return {
        "id": order.id,
        "guest_name": order.guest_name,
        "guest_email": order.guest_email,
        "guest_phone": order.guest_phone,
        "status": order.status,
        "total_price": order.total_price,
        "total_items": order.total_items,
        "created_at": order.created_at,
        "items": order_items_with_details
    }


@router.get("/{order_id}/items", response_model=List[OrderItemSchema])
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    """Get order items for a specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    return order_items


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order (admin only)"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Delete order items first (cascade should handle this, but explicit for safety)
    db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
    
    # Delete the order
    db.delete(order)
    db.commit()
    
    return None
