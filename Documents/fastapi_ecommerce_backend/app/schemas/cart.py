from pydantic import BaseModel
from typing import List, Optional


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(BaseModel):
    quantity: int


class CartItem(CartItemBase):
    id: int
    cart_id: int
    product_name: str
    product_price: int
    total_price: int

    class Config:
        from_attributes = True


class Cart(BaseModel):
    id: int
    items: List[CartItem] = []
    total_items: int = 0
    total_price: int = 0

    class Config:
        from_attributes = True
