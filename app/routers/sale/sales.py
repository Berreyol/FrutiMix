from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import crud
from .. import inventory
from ... import schemas
from ..product.crud import get_product_by_title, get_product_recipe
from ..material.crud import get_material_by_title
from ...dependencies import get_db
from datetime import datetime, date, timezone

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    responses={404: {"description": "Not found"}},
)

def check_stock(db: Session, sale: schemas.Sale):
    for detail in sale.details:
        db_product = get_product_by_title(db, detail.product.title)
        if db_product.is_compose:
            continue
        db_inventory = inventory.products.crud.get_product_inventory(db, db_product.id)
        if db_inventory.quantity < detail.quantity:
            return (detail.product, detail.quantity)
    return True

@router.get("/")
async def find_sales(db: Session = Depends(get_db)):
    return crud.list_sale(db)

@router.get("/{sale_id}")
async def find_sale_by_id(sale_id: int, db: Session = Depends(get_db)):
    return crud.get_sale_by_id(db, sale_id)

@router.get("/today")
async def find_today_sales(db: Session = Depends(get_db)):
    today = date.today()
    return crud.get_sales_by_date(db, today)

@router.get("/{start_date}")
async def find_sale_by_date(start_date: date, db: Session = Depends(get_db)):
    return crud.get_sales_by_date(db, start_date)

@router.get("/{start_date}/{end_date}")
async def find_sales_by_date_range(start_date: date, end_date: date, db: Session = Depends(get_db)):
    return crud.get_sales_by_date_range(db, start_date, end_date)

@router.post("/")
async def save_sale(sale: schemas.Sale, db: Session = Depends(get_db)):
    result = check_stock(db, sale)
    if isinstance(result, tuple):
        raise HTTPException(status_code=400, detail=f"Not enough {result[0].title} in stock")
    for detail in sale.details:
        update_inventory(db, detail)
    db_sale = crud.create_sale(db, sale)
    crud.create_sale_details(db, db_sale.id, sale)
    return db_sale

def update_inventory(db: Session, detail: schemas.SaleDetail):
    def update_product_inventory(product_id: int):
        product_inventory = schemas.ProductInventory(
            product = detail.product,
            quantity = detail.quantity * -1
        )
        inventory.products.crud.update_stock_inventory(
            db, db_product.id, product_inventory)
    
    def update_material_inventory(material_id: int, recipe: schemas.Recipe):
        material_inventory = schemas.MaterialInventory(
            material = recipe.material,
            quantity = recipe.quantity * -1
        )
        inventory.materials.crud.update_stock_inventory(
            db, db_material.id, material_inventory)

    db_product = get_product_by_title(db, detail.product.title)
    if db_product.is_compose:
        for recipe in get_product_recipe(db_product.id, db):
            db_material = get_material_by_title(db, recipe.material.title)
            update_material_inventory(db_material.id, recipe)
    else: 
        update_product_inventory(db_product.id)
    
@router.delete("/")
async def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = crud.get_sale_by_id(db, sale_id)
    if not db_sale:
        raise HTTPException(status_code=400, detail="Product doesn't exists")
    db.delete(db_sale)
    db.commit()
    return {"detail": "Sale deleted successfully!"}

