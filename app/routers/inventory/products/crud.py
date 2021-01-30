from sqlalchemy.orm import Session

from .... import models, schemas
from ...product.crud import get_product_by_title

def list_inventory(db: Session):
    return db.query(models.ProductInventory).all()

def get_product_inventory(db: Session, product_id: int):
    return db.query(models.ProductInventory).filter(models.ProductInventory.product_id == product_id).first()

def create_inventory(db: Session, inventory_detail: schemas.ProductInventory):
    db_product = get_product_by_title(db, inventory_detail.product.title)
    db_inventory = models.ProductInventory(
        product_id = db_product.id,
        quantity = inventory_detail.quantity
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_stock_inventory(db: Session, product_id: int, inventory_detail: schemas.ProductInventory):
    db_inventory = get_product_inventory(db, product_id)
    db_inventory.quantity += inventory_detail.quantity
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, product_id: int, inventory_detail: schemas.ProductInventory):
    db_inventory = get_product_inventory(db, product_id)
    db_inventory.quantity = inventory_detail.quantity
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, product_id: int):
    db_inventory = get_product_inventory(db, product_id)
    db.delete(db_inventory)
    db.commit()