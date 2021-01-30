from sqlalchemy.orm import Session

from ... import models, schemas

def list_materials(db: Session):
    return db.query(models.Material).all()

def get_material_by_id(db: Session, material_id: int):
    return db.query(models.Material).filter(models.Material.id == material_id).first()

def get_material_by_title(db: Session, material_title: str):
    return db.query(models.Material).filter(models.Material.title == material_title).first()

def create_material(db: Session, material: schemas.Material):
    db_material = models.Material(
        title=material.title, 
        cost=material.cost,
        measure=material.measure
        )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def update_material(db: Session, material_id: int, new_material: schemas.Material):
    db_material = get_material_by_id(db, material_id)
    db_material.title = new_material.title
    db_material.measure = new_material.measure
    db_material.cost = new_material.cost
    db.commit()
    db.refresh(db_material)
    return db_material

def delete_material(db: Session, material_id: int):
    db_material = get_material_by_id(db, material_id)
    db.delete(db_material)
    db.commit()