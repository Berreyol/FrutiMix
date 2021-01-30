from sqlalchemy.orm import Session

from ... import models, schemas

def list_categories(db: Session):
    return db.query(models.Category).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_category_by_name(db: Session, category_name: int):
    return db.query(models.Category).filter(models.Category.name == category_name).first()

def create_category(db: Session, category: schemas.Category):
    db_category = models.Category(
        name = category.name,
        description = category.description
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, new_category: schemas.Category):
    db_category = get_category_by_id(db, category_id)
    db_category.name = new_category.name
    db_category.description = new_category.description
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    db.delete(db_category)
    db.commit()