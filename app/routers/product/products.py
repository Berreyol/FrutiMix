from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...dependencies import get_db
from ... import schemas
from . import crud

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_products(db: Session = Depends(get_db)):
    return crud.list_products(db)

@router.get("/active")
async def list_active_products(db: Session = Depends(get_db)):
    return crud.list_active_products(db)

@router.get("/{product_id}")
async def find_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if db_product:
        return schemas.Product(
            title = db_product.title,
            category_name =  db_product.category.name,
            materials = crud.get_product_recipe(product_id, db),
            cost = db_product.cost,
            price = db_product.price,
            is_active = db_product.is_active,
            is_compose = db_product.is_compose
        )
    return None

@router.get("/{product_id}/recipe")
async def find_product_recipe(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product_recipe(product_id, db)

@router.post("/")
async def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_title(db, product.title)
    if db_product:
        raise HTTPException(status_code=400, detail="Product already registered")
    db_category = crud.get_category_by_name(db, product.category_name)
    if not db_category:
        raise HTTPException(status_code=400, detail="Category doesn't exists")
    db_product = crud.create_product(db, product)
    create_recipe(db, db_product.id, product.materials)
    return db_product
    
@router.put("/{product_id}")
async def update_product(product_id: int, new_product: schemas.Product, \
    db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if not db_product:
        raise HTTPException(status_code=400, detail="Product doesn't exists")
    db_category = crud.get_category_by_name(db, new_product.category_name)
    if not db_category:
        raise HTTPException(status_code=400, detail="Category doesn't exists")
    crud.delete_recipe(db, db_product.id)
    create_recipe(db, db_product.id, new_product.materials)
    return crud.update_product(db, product_id, new_product)

async def create_recipe(db: Session, product_id: int, materials: List[schemas.Recipe]):
    for recipe in materials:
        crud.create_recipe(db, product_id, recipe)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if db_product:
        crud.delete_product(db, product_id)
        return {"detail": "Product deleted successfully!"}
    raise HTTPException(status_code=400, detail="Product doesn't exists")
