from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime
from .database import Base

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    cost = Column(Float)
    measure = Column(String)

    inventory = relationship('MaterialInventory')

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)

    products = relationship('Product')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    cost = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Float)
    is_active = Column(Boolean)
    is_compose = Column(Boolean)

    category = relationship('Category')
    recipe = relationship('Recipe', cascade='all, delete-orphan')
    sale = relationship('SaleDetail')
    inventory = relationship('ProductInventory', cascade='all, delete-orphan')

class Recipe(Base):
    __tablename__ = 'recipes'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    quantity = Column(Integer)

    product = relationship('Product')
    material = relationship('Material')

class MaterialInventory(Base):
    __tablename__ = 'material_inventory'

    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    quantity = Column(Integer)

    material = relationship('Material')

class ProductInventory(Base):
    __tablename__ = 'product_inventory'

    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)

    material = relationship('Product')


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, primary_key=True)
    total = Column(Float)

    details = relationship('SaleDetail')
    
class SaleDetail(Base):
    __tablename__ = 'sale_details'

    sale_id = Column(Integer, ForeignKey('sales.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)

    sale = relationship('Sale')
    product = relationship('Product')