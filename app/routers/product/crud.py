from sqlalchemy.orm import Session

from ... import models, schemas
from ..category.crud import get_category_by_name
from ..material.crud import get_material_by_title

def list_products(db: Session):
    return db.query(models.Product).all()

def list_active_products(db: Session):
    return db.query(models.Product).filter(models.Product.is_active == True).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_title(db: Session, product_title: int):
    return db.query(models.Product).filter(models.Product.title == product_title).first()

def create_product(db: Session, product: schemas.Product):
    db_category = get_category_by_name(db, product.category_name)
    db_product = models.Product(
        title=product.title, 
        category_id=db_category.id,
        cost=product.cost,
        price=product.price,
        is_active=product.is_active,
        is_compose=product.is_compose)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
    
def update_product(db: Session, product_id: int, new_product: schemas.Product):
    db_category = get_category_by_name(db, new_product.category_name)
    db_product = get_product_by_id(db, product_id)
    db_product.title = new_product.title
    db_product.category_id = db_category.id
    db_product.cost = new_product.cost
    db_product.price = new_product.price
    db_product.is_active = new_product.is_active
    db_product.is_compose = new_product.is_compose
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id):
    db_product = get_product_by_id(db, product_id)
    db.delete(db_product)
    db.commit()

def get_product_recipe(product_id: int, db: Session):
    db_recipe = get_recipe_by_product(db, product_id)
    return [
        schemas.Recipe(
            material = schemas.Material(
                title = x.material.title,
                measure = x.material.measure,
                cost = x.material.cost),
            quantity = x.quantity)
        for x in db_recipe]
        
def get_recipe_by_product(db: Session, product_id):
    return db.query(models.Recipe).filter(models.Recipe.product_id == product_id).all()

def create_recipe(db: Session, product_id: int, recipe: schemas.Recipe):
    db_material = get_material_by_title(db, recipe.material.title)
    db_recipe = models.Recipe(
        product_id = product_id,
        material_id = db_material.id,
        quantity = recipe.quantity
    )
    db.add(db_recipe)
    db.commit()

def delete_recipe(db: Session, product_id):
    db_recipe = get_recipe_by_product(db, product_id)
    for recipe in db_recipe:
        db.delete(recipe)
    db.commit()