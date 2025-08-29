from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    image: Optional[str] = None
    stock: Optional[int] = 0
    category: Optional[str] = None
    is_active: Optional[bool] = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    image: Optional[str] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True
