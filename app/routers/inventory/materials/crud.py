from sqlalchemy.orm import Session

from .... import models, schemas
from ...material.crud import get_material_by_title

def list_inventory(db: Session):
    return db.query(models.MaterialInventory).all()

def get_material_inventory(db: Session, material_id: int):
    return db.query(models.MaterialInventory).filter(models.MaterialInventory.material_id == material_id).first()

def create_inventory(db: Session, inventory_detail: schemas.MaterialInventory):
    db_material = get_material_by_title(db, inventory_detail.material.title)
    db_inventory = models.MaterialInventory(
        material_id = db_material.id,
        quantity = inventory_detail.quantity
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_stock_inventory(db: Session, material_id: int, inventory_detail: schemas.MaterialInventory):
    db_inventory = get_material_inventory(db, material_id)
    db_inventory.quantity += inventory_detail.quantity
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def update_inventory(db: Session, material_id: int, inventory_detail: schemas.MaterialInventory):
    db_inventory = get_material_inventory(db, material_id)
    db_inventory.quantity = inventory_detail.quantity
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def delete_inventory(db: Session, material_id: int):
    db_inventory = get_material_inventory(db, material_id)
    db.delete(db_inventory)
    db.commit()