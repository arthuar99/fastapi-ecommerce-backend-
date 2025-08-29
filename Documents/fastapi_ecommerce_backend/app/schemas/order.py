from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product_name: str
    product_price: int
    total_price: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    guest_name: str
    guest_email: EmailStr
    guest_phone: str


class Order(OrderCreate):
    id: int
    created_at: datetime
    items: List[OrderItem] = []
    total_items: int = 0
    total_price: int = 0

    class Config:
        from_attributes = True


class OrderSummary(BaseModel):
    id: int
    guest_name: str
    guest_email: str
    created_at: datetime
    total_items: int
    total_price: int

    class Config:
        from_attributes = True
