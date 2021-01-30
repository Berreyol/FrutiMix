from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime    

class Material(BaseModel):
    title: str
    cost: float
    measure: Optional[str]

class Category(BaseModel):
    name: str
    description: Optional[str]

class Recipe(BaseModel):
    material: Material
    quantity: int

class Product(BaseModel):
    title: str
    cost: float
    category_name: str
    materials: List[Recipe]
    price: float
    is_active: bool
    is_compose: bool

class MaterialInventory(BaseModel):
    material: Material
    quantity: int

class ProductInventory(BaseModel):
    product: Product
    quantity: int

class SaleDetail(BaseModel):
    product: Product
    quantity: int

class Sale(BaseModel):
    details: List[SaleDetail]
    total: float